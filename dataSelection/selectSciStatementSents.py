import re
from tqdm import tqdm
from V7.Utils import *
import spacy
nlp = spacy.load("en_core_sci_sm")
sci_statement_words_set_1 = {"Strengths and limitations of the study", "KEY MESSAGES", "Conclusions and Implications", "What New Information Does This Article Contribute", "Novelty and Significance", "HIGHTLIGHTS",
                          "Statement of Contribution", "Whats Known on this Subject", "What This Study Adds","What is New","KEY POINTS","WHAT IS NEW HERE","AUTHOR SUMMARY","Importance","What are the new findings","Strengthslimitations of this study",
                          "Author contributions","What is already known about this subject","Key Findings", "Summary of findings","IMPORTANCE",
                             "Significance", "Summary", "Simple Summary", "STATEMENT", "Strengthslimitations of this trialStrengths", "Conclusions","CONCLUSIONS"}
sci_statement_words_set_2 = {"The new species","We reason", "we find"," conclude that","concluded that", "we found",
                              "The results of the study showed that","we observe" ,"we demonstrate","In contrast",
                             "this work expands", "this work expanded", "showcase",  "it is observed that", "we reveal", "reveals","it was observed that"
                             "we present", "data indicate", "finds","we supported","we discover", "To address this problem",
                             "we raised", "To answer such questions","sought to", "data suggest that","We study that",
                             "This work provides", "These evaluations revealed that","Our study provides","we address",
                             "Our study advances","As a result","we infected","we identified","we revealed","Our study suggests","We confirmed", "Notably","confirm that",
                             "Our estimates suggest","This study provides", "Our study contributes to","To address these challenges","Our exploratory observations","We identify","we characterised",
                             "Our data shows"," In this study,", "we highlight","This study is the first",
                             "The model shows", "we have identified","our work provides", "We also estimate that","we detected", "We previously detected and characterized",
                             "We introduce", "We determine", "highlights", "The study included", "This paper brings","We presumed that","We aimed to study","We studied",
                             "the main novelties", "implicates", "This work suggests that","we define",
                             "Our study summarized","The data we show provides","Our findings", "The research indicates","In contrast,", "Findings suggest","In conclusion,"
                             "Our data show","find that","show that","showed that", "we report that","The fact that","Here, we study","Here, we studied","Here, we study that","Here, we studied that",
                             "In summary,", "These results demonstrate","The results highlight",
                             "these results suggest that","Our results","our study presents","This study supports","We also reported evidence","These results reveal that","Our main findings","This work is the first","Here we presented"," we hypothesized that"," In this work, we study", "These findings provide"
                             "indicating","Our results highlight","indicates","Highlights-"}
sci_statement_words_set_2_new = set([word.lower() for word in sci_statement_words_set_2])
sci_statement_words_set_3 = {"DISCUSSION","In brief",  "Discussion and Conclusion", "Interpretation",
                             "MAIN CONCLUSIONS","Discussion and conclusions"} # -1

def select_sent_w_sci_statement_words_for_abs_extra(id_to_abss,sci_set_words):
    _selected_sents_for_abss_w_id = []
    not_statement_abs = []
    for _,_abs in tqdm(enumerate(id_to_abss), total=len(id_to_abss)):
        _selected_sents_for_abss = []
        abs_ = _abs[1]
        for sci_word in sci_set_words:
            re_str = r'(?=[^.\n])('+ sci_word +')+([\w\s\,\.\%\-\{\}\(\)\/\:\{\}\;\+\"\"\>\<\?\=\~\'\']*)'
            pattern = re.compile(re_str, flags=re.M)
            match_res = pattern.findall(abs_)
            if len(match_res) != 0:
                for _match_ele in match_res:
                    selected_sents = ' '.join(_match_ele)
                    selected_sents = re.sub("  ", " ", selected_sents)
                    if selected_sents[-1] != '.':
                        selected_sents += '.'
                    _selected_sents_for_abss.append(selected_sents)
                    abs_ = abs_.replace(selected_sents, "")


        if len(_selected_sents_for_abss) == 0:
            not_statement_abs.append(_abs)
        else:
            _selected_sents_for_abss_w_id.append((_abs[0], ' '.join(_selected_sents_for_abss)))

    return _selected_sents_for_abss_w_id, not_statement_abs

def select_sent_w_sci_statement_words_for_abs(id_to_abss,sci_set_words):
    _selected_sents_for_abss_w_id = []
    not_statement_abs = []
    for _,_abs in tqdm(enumerate(id_to_abss), total=len(id_to_abss)):
        _selected_sents_for_abss = []
        abs_ = _abs[1]
        for sci_word in sci_set_words:
            re_str = r'(?=[^.\n])('+ sci_word +')+([\w\s\,\.\%\-\{\}\(\)\/\:\{\}\;\+\"\"\>\<\?\=\~\'\']*)'
            pattern = re.compile(re_str, flags=re.M)
            match_res = pattern.findall(abs_)
            if len(match_res) != 0:
                for _match_ele in match_res:
                    selected_sents = ' '.join(_match_ele)
                    selected_sents = re.sub("  ", " ", selected_sents)
                    if selected_sents[-1] != '.':
                        selected_sents += '.'
                    _selected_sents_for_abss.append(selected_sents)
                    abs_ = abs_.replace(selected_sents, "")


        if len(_selected_sents_for_abss) == 0:
            not_statement_abs.append(_abs)
        else:
            _selected_sents_for_abss_w_id.append((_abs[0], ' '.join(_selected_sents_for_abss)))

    return _selected_sents_for_abss_w_id, not_statement_abs

def select_sent_w_sci_statement_intra_sents(id_to_abss,sci_set_words):
    _selected_sents_for_abss_w_id = []
    not_statement_abs = []

    for _,_abs in tqdm(enumerate(id_to_abss), total=len(id_to_abss)):
        _selected_sents_for_abss = []
        abs_ = _abs[1]
        # sents = sents_split_for_one_abstract(abs_)
        doc = nlp(abs_)
        sents = doc.sents
        for sent in sents:
            for sci_word in sci_set_words:
                re_str = r'(?=[^.])([\[\]\w\s\,\.\%\-\{\}\(\)\/\:\{\}\;\+\"\"\>\<\?\=\~\'\'\&]*'+ sci_word +')([\w\s\,\.\%\-\{\}\(\)\/\:\{\}\;\+\"\"\>\<\?\=\~\'\'\[\]\&]*)'
                pattern = re.compile(re_str, flags=re.M | re.I)
                match_res = pattern.findall(sent.text)
                if len(match_res) != 0:
                    for _match_ele in match_res:
                        selected_sents = ' '.join(_match_ele)
                        selected_sents = re.sub("  ", " ",selected_sents)
                        if selected_sents[-1] != '.':
                            selected_sents += '.'
                        if selected_sents not in _selected_sents_for_abss:
                            _selected_sents_for_abss.append(selected_sents)
                            abs_ = abs_.replace(selected_sents, "")

        if len(_selected_sents_for_abss) == 0:
            not_statement_abs.append(_abs)
        else:
            _selected_sents_for_abss_w_id.append((_abs[0], ' '.join(_selected_sents_for_abss)))

    return _selected_sents_for_abss_w_id, not_statement_abs



def select_more_turns(id_to_abss,sci_set_words):
    _selected_, _not_selected = select_sent_w_sci_statement_intra_sents(id_to_abss, sci_set_words)
    return _selected_, _not_selected

