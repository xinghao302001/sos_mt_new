﻿import torch
import numpy as np
from transformers import BertTokenizer
import pandas as pd
from torch import nn
from transformers import BertModel
from torch.optim import Adam
from tqdm import tqdm

np.random.seed(112)
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

bio_sta_sents = pd.read_csv('bio_sta_selected_wo_marker.csv',
                            usecols=['sents',"labels"],
                            dtype={
                                "sents": str,
                                'labels':int
                            }
                            )
not_bio_sta_sents = pd.read_csv('not_bio_sta_selected_wo_marker.csv',
                            usecols=["sents", 'labels'],
                            dtype={
                                "sents": str,
                                'labels': int
                            }
                            )
bio_sta_sents_samples = bio_sta_sents.sample(700,random_state=42).reset_index(drop=True)
all_df = pd.concat([bio_sta_sents_samples,not_bio_sta_sents],axis=0).reset_index(drop=True)


df_train, df_val, df_test = np.split(all_df.sample(frac=1, random_state=42).reset_index(drop=True),
                                     [int(.8*len(all_df)), int(.9*len(all_df))])

df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

class Dataset(torch.utils.data.Dataset):
    def __init__(self, df):
        self.labels = df['labels'].tolist()
        self.texts = [tokenizer(text, padding='max_length',
                                max_length=512, truncation=True,
                                return_tensors="pt") for text in df['sents']]

    def classes(self):
        return self.labels

    def __len__(self):
        return len(self.labels)

    def get_batch_labels(self,idx):
        return np.array(self.labels[idx])

    def get_batch_texts(self,idx):
        return self.texts[idx]

    def __getitem__(self, idx):
        batch_texts = self.get_batch_texts(idx)
        batch_y = self.get_batch_labels(idx)

        return batch_texts, batch_y

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


def train(model, train_data, val_data, learning_rate, epochs):
    train, val = Dataset(train_data), Dataset(val_data)

    train_dataloader = torch.utils.data.DataLoader(train, batch_size=2, shuffle=True)
    val_dataloader = torch.utils.data.DataLoader(val, batch_size=2)

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=learning_rate)

    if use_cuda:
        model = model.cuda()
        criterion = criterion.cuda()

    for epoch_num in range(epochs):

        total_acc_train = 0
        total_loss_train = 0

        for train_input, train_label in tqdm(train_dataloader):
            train_label = train_label.to(device)
            mask = train_input['attention_mask'].to(device)
            input_id = train_input['input_ids'].squeeze(1).to(device)

            output = model(input_id, mask)

            batch_loss = criterion(output, train_label.long())
            total_loss_train += batch_loss.item()

            acc = (output.argmax(dim=1) == train_label).sum().item()
            total_acc_train += acc

            model.zero_grad()
            batch_loss.backward()
            optimizer.step()

        total_acc_val = 0
        total_loss_val = 0

        with torch.no_grad():

            for val_input, val_label in val_dataloader:
                val_label = val_label.to(device)
                mask = val_input['attention_mask'].to(device)
                input_id = val_input['input_ids'].squeeze(1).to(device)

                output = model(input_id, mask)

                batch_loss = criterion(output, val_label.long())
                total_loss_val += batch_loss.item()

                acc = (output.argmax(dim=1) == val_label).sum().item()
                total_acc_val += acc

        print(
            f'Epochs: {epoch_num + 1} | Train Loss: {total_loss_train / len(train_data): .3f} \
            | Train Accuracy: {total_acc_train / len(train_data): .3f} \
            | Val Loss: {total_loss_val / len(val_data): .3f} \
            | Val Accuracy: {total_acc_val / len(val_data): .3f}')


def evaluate(model, test_data):
    test = Dataset(test_data)

    test_dataloader = torch.utils.data.DataLoader(test, batch_size=2)

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    if use_cuda:
        model = model.cuda()

    total_acc_test = 0
    with torch.no_grad():

        for test_input, test_label in test_dataloader:
            test_label = test_label.to(device)
            mask = test_input['attention_mask'].to(device)
            input_id = test_input['input_ids'].squeeze(1).to(device)

            output = model(input_id, mask)

            acc = (output.argmax(dim=1) == test_label).sum().item()
            total_acc_test += acc

    print(f'Test Accuracy: {total_acc_test / len(test_data): .3f}')



# if __name__=="__main__":
#     EPOCHS = 5
#     model = BertClassifier()
#     LR = 1e-6
#     train(model, df_train, df_val, LR, EPOCHS)
#     evaluate(model, df_test)



