import re
from tqdm import tqdm
from Utils import *
import spacy
nlp = spacy.load("en_core_sci_sm")


def select_sent_w_sci_statement_words_for_abs_extra(id_to_abss,sci_set_words):
    '''
        select sentences/paragraphs that Section Names which indicate statement
        :param id_to_abss: list
        :param sci_set_words: set
        :return:
    '''
    _selected_sents_for_abss_w_id = []
    not_statement_abs = []
    for _,_abs in tqdm(enumerate(id_to_abss), total=len(id_to_abss)):
        _selected_sents_for_abss = []
        abs_ = _abs[1]
        for sci_word in sci_set_words:
            # TODO check regular expression
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
    '''
        select sentences/paragraphs that Section Names which indicate statement
        :param id_to_abss: list
        :param sci_set_words: set
        :return:
    '''
    _selected_sents_for_abss_w_id = []
    not_statement_abs = []
    for _,_abs in tqdm(enumerate(id_to_abss), total=len(id_to_abss)):
        _selected_sents_for_abss = []
        abs_ = _abs[1]
        for sci_word in sci_set_words:
            # TODO check regular expression
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
    '''
       select sentences by sci_word_sets that indicate statments.
            :param id_to_abss: list
            :param sci_set_words: set
            :return:
    '''
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
                # TODO check regular expression
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
    '''
           select sentences with more turns.
    '''
    _selected_, _not_selected = select_sent_w_sci_statement_intra_sents(id_to_abss, sci_set_words)
    return _selected_, _not_selected

