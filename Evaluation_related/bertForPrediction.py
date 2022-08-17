import torch
import numpy as np
from transformers import BertTokenizer
import pandas as pd
from torch import nn
from transformers import BertModel
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

np.random.seed(112)
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')


import torch
class DatasetforPredict(torch.utils.data.Dataset):
    def __init__(self, df):
        self.texts = [tokenizer(text, padding='max_length',
                                max_length=512, truncation=True,
                                return_tensors="pt") for text in df['sents']]
        self.orignal_texts = [text for text in df['sents']]
    def __len__(self):
        return len(self.texts)

    def get_batch_texts(self,idx):
        return self.texts[idx]
    def get_batch_original_texts(self,idx):
        return self.orignal_texts[idx]

    def __getitem__(self, idx):
        batch_texts = self.get_batch_texts(idx)
        batch_orginal_texts = self.get_batch_original_texts(idx)
        return batch_texts, batch_orginal_texts
class BertClassifier(nn.Module):
    def __init__(self,dropout=0.5):
        super(BertClassifier, self).__init__()


        self.bert = BertModel.from_pretrained('bert-base-cased')
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768,2)
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):
        _, cls_output = self.bert(input_ids=input_id, attention_mask=mask, return_dict=False)
        dropout_output = self.dropout(cls_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)
        return final_layer

def predict(load_model, predict_data):
    '''
    :predict the label of the input sents
    '''
    predict = DatasetforPredict(predict_data)

    predict_dataloader = torch.utils.data.DataLoader(predict)

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    if use_cuda:
        load_model = load_model.cuda()


    with torch.no_grad():
        predict_res = []
        for predict_bert_input, predict_original_text in predict_dataloader:
            # test_label = test_label.to(device)
            mask = predict_bert_input['attention_mask'].to(device)
            input_id = predict_bert_input['input_ids'].squeeze(1).to(device)
            m = nn.Sigmoid()
            output = load_model(input_id, mask)
            output_Sigmoid = m(output.argmax(dim=1))
            if output_Sigmoid > 0.5:
                predict_label = 1
                predict_res.append((predict_label, predict_original_text))
            else:
                predict_label = 0
                predict_res.append((predict_label, predict_original_text))
        return predict_res



# if __name__=="__main__":
#     bio_sta_sents = pd.read_csv('bio_sta_selected_wo_marker.csv',
#                                 usecols=['sents', "labels"],
#                                 dtype={
#                                     "sents": str,
#                                     'labels': int
#                                 }
#                                 )
#     not_bio_sta_sents = pd.read_csv('not_bio_sta_selected_wo_marker.csv',
#                                     usecols=["sents", 'labels'],
#                                     dtype={
#                                         "sents": str,
#                                         'labels': int
#                                     }
#                                     )
#     bio_sta_sents_samples = bio_sta_sents.sample(700, random_state=42).reset_index(drop=True)
#     all_df = pd.concat([bio_sta_sents_samples, not_bio_sta_sents], axis=0).reset_index(drop=True)
#
#     df_train, df_val, df_test = np.split(all_df.sample(frac=1, random_state=42).reset_index(drop=True),
#                                          [int(.8 * len(all_df)), int(.9 * len(all_df))])
#
#     df_train = df_train.reset_index(drop=True)
#     df_val = df_val.reset_index(drop=True)
#     df_test = df_test.reset_index(drop=True)
#
#
#     model = torch.load('sci_state_verification.pt',map_location=torch.device('cpu'))
#     res = predict(model, df_test)
#     print(model)