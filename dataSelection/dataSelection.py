import pandas as pd
import re
from selectSciStatementSents import *


##### define more sci statement word sets #####
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
sci_statement_words_set_4 = {"find","Here, we present", "these data establish","Conclusion","revealed","In conclusion,"} # -2
sci_stamement_words_set_5 = {"our data provide strong evidence","show","our data provide strong evidence","we analyzed","we report","this data suggests","we utilized","Finally, we performed","this is the first report", "More specifically,","leads to",
                             "Author summary","It has been demonstrated that","identified"}  # -3
sci_stamement_words_set_6 = {"Interestingly, ", "Our data provide the first direct evidence that","resulted in", " indicating", "are likely responsible for"} # -4
sci_stamement_words_set_7 = {"Results","In clear contrast,","we complemented their characterization","Surprisingly, ","we provide evidence that ","We provide molecular evidence that ","We established","we propose that"} # -5

def read_data(path, flags=1):
    if flags == 1:
        data = pd.read_csv(path,
                           usecols=["id", "title", "posted", 'abstract'],
                           dtype={
                               "id": str,
                               "title": str,
                               'posted': str,
                               'abstract': str
                           },

                           parse_dates=['posted'],
                           )
    else:
        data = pd.read_csv(path,
                           usecols=["id", "abstract"],
                           dtype={
                               "id": str,
                               "abstract": str,
                           }
                           )
    abs_lists = data['abstract'].tolist()
    id_lists = data['id'].tolist()
    return id_lists, abs_lists


def data_selections(abss_id, abss_list, sci_set,flags):
    '''
    main function for data selection using some Wrappers defined from selectSciStatementSents.py
    :param abss_id: list
    :param abss_list: list
    :param sci_set: sci_word set
    :param flags: the n-th turn selection
    :return:
    '''

    ### round = 1, select sentences with sci_set_1, sci_set_2, and sci_set_3
    if flags == 1:
        id_to_abss = list(zip(abss_id,abss_list))
        # first_selected_sents_for_abss_w_id, not_bio_abs_id = bio_filtering_for_abs(id_to_abss)
        first_selected_sents_for_abss, not_statement_abs_a = select_sent_w_sci_statement_words_for_abs(id_to_abss,sci_statement_words_set_3)
        # first_kids_selected_sents, not_statement_abs_b = select_sent_w_sci_statement_intra_sents(first_selected_sents_for_abss)
        second_selected_sents_for_abss, not_statement_abs_b = select_sent_w_sci_statement_words_for_abs_extra(not_statement_abs_a,sci_statement_words_set_1)
        third_selected_sents_for_abss, not_statement_abs_c = select_sent_w_sci_statement_intra_sents(not_statement_abs_b,sci_statement_words_set_2_new)

        final_selected_sents_for_abs = first_selected_sents_for_abss + third_selected_sents_for_abss + second_selected_sents_for_abss
        final_not_statement_sents_for_abs = not_statement_abs_c

    ### round = n, select sentences with sci_set_4, sci_set_5, sci_set_6, sci_set_7. sci_set...
    else:
        id_to_abss = list(zip(abss_id, abss_list))
        final_selected_sents_for_abs, final_not_statement_sents_for_abs = select_more_turns(id_to_abss,
                                                                                            sci_set_words=sci_set)
    return final_selected_sents_for_abs, final_not_statement_sents_for_abs


def rewrite_selected_sents(seletced_,not_selected_,_selected_path, not_selected_path,flag=False):
    if flag == True:
        data_df = pd.DataFrame(columns=['id','abstract'])
        data_id = []
        data_abs =[]
        for ele_ in seletced_:
            data_id.append(ele_[0])
            data_abs.append(ele_[1])

        data_df['id'] = data_id
        data_df['abstract'] = data_abs

        data_df.to_csv(_selected_path, index=False, encoding='utf-8', index_label=False)

        ### write_no_selected
        data_df_no = pd.DataFrame(columns=['id', 'abstract'])
        data_id_no = []
        data_abs_no = []
        for ele_ in not_selected_:
            data_id_no.append(ele_[0])
            data_abs_no.append(ele_[1])

        data_df_no['id'] = data_id_no
        data_df_no['abstract'] = data_abs_no

        data_df_no.to_csv(not_selected_path, index=False, encoding='utf-8', index_label=False)
        return
    else:
        data_df = pd.DataFrame(columns=['id', 'abstract'])
        data_id = []
        data_abs = []
        for ele_ in seletced_:
            data_id.append(ele_[0])
            data_abs.append(ele_[1])

        data_df['id'] = data_id
        data_df['abstract'] = data_abs

        data_df.to_csv(_selected_path, index=False, encoding='utf-8', index_label=False)
        return


if __name__ == "__main__":
    id_lists, abs_lists = read_data('final_not_selected_w_marker_4.csv',flags=6)
    final_selected_sents_for_abs,not_statement_abs = data_selections(id_lists, abs_lists, sci_stamement_words_set_7, flags=6)
    rewrite_selected_sents(final_selected_sents_for_abs, not_statement_abs, 'final_selected_w_marker_5.csv',
                           'final_not_selected_w_marker_5.csv',flag=True)

    print(final_selected_sents_for_abs)

