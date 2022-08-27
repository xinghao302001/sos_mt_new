'''
    :data preprocess for MetaMap and obtain the results from MetaMap
    input: cleaned and cr_resolved data
    output: results from Metamap
'''
from Utils import *
from MetaMap import *
import pandas as pd
from tqdm import tqdm

def read_data(path):
    data = pd.read_csv(path,
                       usecols=["id", "title","posted",'abstract'],
                       dtype={
                           "id":str,
                           "title":str,
                           'posted': str,
                           'abstract': str
                       },
                       parse_dates=['posted'],
                       )
    abstracts = data['abstract'].tolist()
    return abstracts


'''
    : clean abstracts again
'''
def clean_and_split_abs_for_metamap(coref_resolved_abstracts):
    abstracts_to_sents = []
    for _abs in coref_resolved_abstracts:
        abs_ = remove_characters(_abs)
        sents = nltk.sent_tokenize(abs_)
        abstracts_to_sents.append(sents)
    return abstracts_to_sents

'''
    : get MetaMap results from MetaMap
'''
def getMetamapRes(abs_to_sents_list):
    mmres = []
    for _, para in tqdm(enumerate(abs_to_sents_list),total=len(abs_to_sents_list)):
        para_mms_res = []
        for sent in para:
            sent_res = get_metamap_output(sent)
            para_mms_res.append(sent_res)
        mmres.append(para_mms_res)
    return mmres

'''
    : writing in json file, including None output file
'''
def write_mmres(mmRes):
    with open('data/mmres_0817A.json','w',encoding='utf-8') as fw:
        for ele in mmRes:
            jsObj = json.dumps(ele)
            fw.write(jsObj)
            fw.write("\n")
        fw.close()
    return




if __name__ =="__main__":
    coref_abs = read_data("data/coref_resolved_data.csv")
    clean_for_metamap = clean_and_split_abs_for_metamap(coref_abs)
    mmres = getMetamapRes(clean_for_metamap)
    write_mmres(mmres)
