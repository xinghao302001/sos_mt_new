import re
import pandas as pd
from V7.Utils import *
from tqdm import tqdm
import numpy as np
from V7.selectBioSentsBERN2 import bio_filtering_for_sent

sci_statement_words_set_1 = {"Strengths and limitations of the study", "KEY MESSAGES", "Conclusions and Implications", "What New Information Does This Article Contribute", "Novelty and Significance", "HIGHTLIGHTS",
                          "Statement of Contribution", "Whats Known on this Subject", "What This Study Adds","What is New","KEY POINTS","WHAT IS NEW HERE","AUTHOR SUMMARY","Importance","What are the new findings","Strengthslimitations of this study",
                          "Author contributions","What is already known about this subject","Key Findings", "Summary of findings","IMPORTANCE",
                          "Significance", "Summary", "Simple Summary", "STATEMENT", "Strengthslimitations of this trialStrengths", "Conclusions","CONCLUSIONS","Significance Statement"}
sci_statement_words_set_2 = {"The new species","We reason", "We find"," conclude that","concluded that", "We found",
                              "The results of the study showed that","We observe" ,"We demonstrate","In contrast",
                             "this work expands", "this work expanded", "showcase",  "It is observed that", "We reveal", "reveals","it was observed that"
                             "We present", "data indicate", "finds","We supported","we discover", "To address this problem",
                             "We raised", "To answer such questions","sought to", "data suggest that","We study that",
                             "This work provides", "These evaluations revealed that","Our study provides","We address",
                             "Our study advances","As a result","we infected","we identified","we revealed","Our study suggests","We confirmed", "Notably","confirm that",
                             "Our estimates suggest","This study provides", "Our study contributes to", "In this work","To address these challenges","Our exploratory observations","We identify","we characterised",
                             "Our data shows"," In this study,", "we highlight","This study is the first",
                             "The model shows", "We have identified","Our work provides", "We also estimate that","We detected", "We previously detected and characterized",
                             "We introduce", "We determine", "highlights", "The study included", "This paper brings","We presumed that","We aimed to study","We studied",
                             "the main novelties", "implicates", "This work suggests that","we define",
                             "Our study summarized","The data we show provides","Our findings", "The research indicates","In contrast,", "Findings suggest","In conclusion,"
                             "Our data show","find that","show that","showed that", "We report that","The fact that","Here, we study","Here, we studied","Here, we study that","Here, we studied that",
                             "In summary,", "indicating that","These results demonstrate","The results highlight",
                             "these results suggest that","Our results","our study presents","This study supports","We also reported evidence","These results reveal that","Our main findings","This work is the first","Here we presented"," we hypothesized that"," In this work, we study", "These findings provide"}
sci_statement_words_set_2_new = set([word.lower() for word in sci_statement_words_set_2])
sci_statement_words_set_3 = {"DISCUSSION","In brief",  "Discussion and Conclusion", "Interpretation",
                             "MAIN CONCLUSIONS","Discussion and conclusions","Highlights"}
sci_statement_words_set_4 = {"Our data show that","Our findings show that","These data show that","In this study","Our data suggest that","these results suggest that","These findings show that","These findings suggest that","The study concluded that","These finds show that","our study presents","we find","Our results showed that","we found that","we define","we identify","our study highlights","Our study demonstrates","we demonstrate that","we further showed that","our results suggest that","This study highlights","we showcase","These data indicate that","we demonstrate","we confirm that","we report that",
                             "Our findings suggest","This study show that","Our findings confirm that","Our results show that", "Our estimates suggest","Our data shows","Our study reveals","Discussion and conclusions","iii\)","ii\)","i\)","we show that","we also show that","we find that","we found that","we conclude that","we showed that",
                             "results show that","Here we show that","Here we define","Here we demonstrate that","Here we demonstrate"}

data_selected = pd.read_csv('final_selected_w_marker.csv',
                            usecols=["id", 'abstract'],
                            dtype={
                                "id": str,
                                'abstract': str
                            }
                            )

data_selected_abs = data_selected['abstract'].tolist()[:50]
all_selected_statement_sents = []
revisited = []
for _,ele_ in tqdm(enumerate(data_selected_abs), total=len(data_selected_abs)):
    sents = sents_split_for_one_abstract(ele_)
    for sent in sents:
        if sent not in revisited:
            revisited.append(sent)
            for sci_word in sci_statement_words_set_3:
                re_str = r'^' + sci_word
                sent = re.sub(r'^\s', '', sent, flags=re.M)
                sent = re.sub(re_str, '', sent)
                sent = re.sub(r'^\s', '', sent, flags=re.M)
            for sci_word in sci_statement_words_set_1:
                re_str = r'^' + sci_word
                sent = re.sub(r'^\s', '', sent, flags=re.M)
                sent = re.sub(re_str, '', sent)
                sent = re.sub(r'^\s', '', sent, flags=re.M)
            for sci_word in sci_statement_words_set_4:
                re_str = r'^' + sci_word
                sent = re.sub(r'^\s', '', sent, flags=re.M)
                sent = re.sub(r'^Therefore|Here|Moreover|Similarly|Notably|Further|Overall|[0-9]+\)|However|Next|Specifically|Finally(?=[\s\,])', '', sent, flags=re.M)
                sent = re.sub(r'^\s|,', '', sent, flags=re.M)
                sent = re.sub(r'^\)|\,', '', sent, flags=re.M)
                sent = re.sub(re_str, '', sent,flags=re.M|re.I)
                sent = re.sub(r'^that', '', sent, flags=re.M | re.I)
                sent = re.sub(r'^\s', '', sent, flags=re.M)
            sent = re.sub(r'^\s|\,|\),|', '', sent, flags=re.M)
            sent = sent.capitalize()
            if len(sent.split()) > 6:
                all_selected_statement_sents.append(sent)

# all_bio_sents = bio_filtering_for_sent(all_selected_statement_sents)
data_selected_w_label = pd.DataFrame(columns=["sents","labels"])
data_selected_w_label["sents"] = all_selected_statement_sents
data_selected_w_label["labels"] = np.ones(len(all_selected_statement_sents))

print(all_selected_statement_sents)
