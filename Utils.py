import nltk
import re
import contractions
import Levenshtein
from collections.abc import Iterable

def read_abstracts(path):
    all_abstracts = []
    with open(path, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            all_abstracts.append(line.strip('\n'))
        filtered_abstracts = list(filter(None,all_abstracts))
    return filtered_abstracts

def sents_split_for_all_abstracts(abstracts_paras):
    all_sents = []
    for _para in abstracts_paras:
        sents = nltk.sent_tokenize(_para)
        for _sent in sents:
            all_sents.append(_sent)

    return all_sents
def sents_split_for_one_abstract(abstract):
    sents = nltk.sent_tokenize(abstract)
    return sents
def remove_characters(sent):
    # sent = sent.strip()
    res_1 = re.sub(r'https?:\/\/.\S+','', sent)
    res_1 = re.sub(r'[a-zA-Z]+://[^\s]*', '', res_1)
    res_1 = re.sub(r'p\<[0-9]\.[0-9]|\(p\<[0-9]\.[0-9]\)','',res_1)
    res_1 = re.sub(r'P\<[0-9]\.[0-9]|\(p\<[0-9]\.[0-9]\)', '', res_1)
    res = re.sub(r'[\?|\$|\&|\*|\%|\@|\(|\)\[\]\{\}\~|;|\’|\”|\‘|“|\'|\=|\>|\¥|\"|\≈|\â|\"|\"]', '', res_1,flags=re.M)
    # res = re.sub(r'[?|$|&|*|%|@|\(|\)\[\]\{\}\~|;|\’|\”]', '', res_1)
    return res

def remove_contractions(sent):
    tmp = contractions.fix(sent)
    return tmp

def bkdr_hash(str, seed=131):
    hash = 0
    for s in str:
        hash = hash*seed + ord(s)
    return hash & 0x7fffffff

def common_words_hash(str1, str2):
    words = str1.strip().split(' ')
    str1_hashset = set(bkdr_hash(word) for word in words)
    common_words = []
    for word in str2.strip().split(' '):
        if bkdr_hash(word) in str1_hashset:
            common_words.append(word)
    if len(common_words) != 0:
        return True
    return False

def str_sim(a,b):
    return Levenshtein.ratio(a, b)

def list_to_str(tokens):
    if isinstance(tokens, Iterable):
        return ' '.join([item for item in tokens])
    else:
        return ''





