from stanfordcorenlp import StanfordCoreNLP
import json
import re
import pandas as pd
from tqdm import tqdm

nlp = StanfordCoreNLP('http://localhost', port=9000)
props = {'annotators': 'tokenize,ssplit,coref',
       'pipelineLanguage':'en',
       'outputFormat':'json'}


def _eval_corefs(json_corefs):
    for k, chain in json_corefs.items():
        if k == "corefs":
            all_corefs = {}
            if len(chain) >= 1:
                for r in chain.values():
                    if len(r) != 0:
                        for n in r:
                            if n['isRepresentativeMention']:
                                representative = n['text']
                        for m in r:
                            if not m['isRepresentativeMention']:
                                all_corefs['{}:{},{}'.format(m['sentNum'], m['startIndex'], m['endIndex'])] = representative.strip()

    return all_corefs

def _replace(s_index, token, corefs):
    t_index = token['index']

    for key in corefs.keys():
        if key.startswith(str(s_index) + ':'):
            s, coref_range = key.strip().split(':', 1)
            coref_range_start, coref_range_end = coref_range.strip().split(',', 1)

            if t_index in range(int(coref_range_start), int(coref_range_end)):

                if t_index == int(coref_range_start):
                    return corefs[key]

                return ''

    return None

def _rebuild_contents(json_sentences, all_corefs):
    resolved = ''
    s_index = 0
    for sentences in json_sentences:
        s_index += 1
        for token in sentences['tokens']:
            replacement = _replace(s_index, token, all_corefs)

            if replacement is None:
                resolved += token['originalText'] + ' '
            elif not replacement is '':
                resolved += replacement + ' '

    return resolved


def get_resolved_texts(text):
    annotated_res = nlp.annotate(text, properties=props)
    _res = json.loads(annotated_res)
    all_cores = _eval_corefs(_res)
    resolved_contents = _rebuild_contents(_res['sentences'],all_cores)
    ## TODO space elimitation optimization
    resolved_contents = resolved_contents.replace(' - ', '-')
    resolved_contents = resolved_contents.replace(' , ', ', ')
    resolved_contents = resolved_contents.replace(' . ', '. ')

    return resolved_contents


if __name__ == "__main__":
    original_data = pd.read_csv('data/cleaned_data_mod_3.csv',
                       usecols=["id", "title", "posted", 'abstract'],
                       dtype={
                           "id": str,
                           "title": str,
                           'posted': str,
                           'abstract': str
                       },

                       parse_dates=['posted'],
                       )
    probe_length = 40
    abstracts = original_data['abstract'].tolist()[:probe_length]
    coref_resolved_abs = []
    for _, _abs in tqdm(enumerate(abstracts),total=len(abstracts)):
        tmp = get_resolved_texts(_abs)
        coref_resolved_abs.append(tmp)

    coref_resolved_abs_df = pd.DataFrame(coref_resolved_abs,columns=["abstract"])
    coref_resolved_data = pd.concat([original_data['id'][:probe_length], original_data['title'][:probe_length],
                                     original_data['posted'][:probe_length], coref_resolved_abs_df], axis=1)
    coref_resolved_data.to_csv('data/coref_resolved_data.csv', index=False, encoding='utf-8', index_label=False)
    print(abstracts)
