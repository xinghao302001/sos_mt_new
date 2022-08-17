import json
from svo_openIE import getSVOs
from Utils import *
import spacy
from tqdm import tqdm

nlp = spacy.load("en_core_web_sm")


# =================================================================================#
def handleMMres(mmres_filepath):
    mmres = []
    with open(mmres_filepath, 'r', encoding="utf-8") as fr:
        for res in fr.readlines():
            dic = json.loads(res)
            mmres.append(dic)
    fr.close()

    all_paras_UttTexts = []
    all_paras_sems = []
    no_map_para_sent_pairs = []
    for i,para in enumerate(mmres):
        para_UttTexts = []
        sent_all_sems = []
        for j,sent in enumerate(para):
            try:
                phrases = sent['AllDocuments'][0]['Document']['Utterances'][0]['Phrases']
                UttText = sent['AllDocuments'][0]['Document']['Utterances'][0]['UttText']
            except:
                no_map_para_sent_pairs.append((i,j))
            mmap_phrases_txt = []
            phrase_to_sem = {}

            for phrase in phrases:
                phrase_text = phrase['PhraseText']
                mmap_phrases_txt.append(phrase_text)

                ## stores all the mapped entities for one sent
                _phrase_mapsem = []
                if len(phrase['Mappings']) == 0:
                    continue
                # get mappings
                mappings = phrase['Mappings']
                _map_sem = []
                for _mapping in mappings:
                    map_cand = _mapping['MappingCandidates']
                    for _map_cand_ele in map_cand:
                        map_sem = _map_cand_ele["SemTypes"]
                        _map_sem.append(','.join(map_sem))
                _phrase_mapsem.append(','.join(_map_sem))
                _phrase_mapsem_del_dupl = list(set(_phrase_mapsem[0].split(',')))
                phrase_to_sem[phrase_text] = _phrase_mapsem_del_dupl

            sent_all_sems.append(phrase_to_sem)
            para_UttTexts.append(UttText)

        all_paras_UttTexts.append(para_UttTexts)
        all_paras_sems.append(sent_all_sems)
    return all_paras_UttTexts, all_paras_sems



# ======================================================================================= #

def getSVOs_w_sem_and_wo_sem(all_paras_uttexts,all_paras_Sems):
    all_svos_wo_sem = []
    all_svos_w_sem = []

    for i,para in tqdm(enumerate(all_paras_uttexts), total=len(all_paras_uttexts)):
        para_sems = all_paras_Sems[i]
        para_triplets_w_sem = []
        para_triplets_wo_sem = []

        for j, utt in enumerate(para):
            ##TODO
            u_doc = nlp(utt)

            utt_svos = getSVOs(u_doc.text)
            # print(utt_svos)

            sent_sem_keys = list(para_sems[j].keys())
            sent_triplet_w_sem = []
            sent_triplet_wo_sem = []

            if len(utt_svos) != 0:
                _triplets_w_sem_to_scores = {}
                _triplets_wo_sem_to_scores = {}
                for triplet in utt_svos:
                    _sub = triplet[0]
                    _verb = triplet[1]
                    _obj = triplet[2]

                    sim_sub = [str_sim(k, _sub) for k in sent_sem_keys]
                    sim_sub_max_score = max(sim_sub)
                    sim_sub_max_index = sim_sub.index(max(sim_sub))
                    sim_verb = [str_sim(k, _verb) for k in sent_sem_keys]
                    sim_verb_max_score = max(sim_verb)
                    sim_verb_max_index = sim_verb.index(max(sim_verb))
                    sim_obj = [str_sim(k, _obj) for k in sent_sem_keys]
                    sim_obj_max_score = max(sim_obj)
                    sim_obj_max_index = sim_obj.index(max(sim_obj))

                    _sub_sem_key = sent_sem_keys[sim_sub_max_index]
                    _sub_sem = para_sems[j].get(_sub_sem_key)
                    _verb_sem_key = sent_sem_keys[sim_verb_max_index]
                    _verb_sem = para_sems[j].get(_verb_sem_key)
                    _obj_sem_key = sent_sem_keys[sim_obj_max_index]
                    _obj_sem = para_sems[j].get(_obj_sem_key)

                    sub_w_sem = _sub + '[' + list_to_str(_sub_sem) + ']'
                    verb_w_sem = _verb + '[' + list_to_str(_verb_sem) + ']'
                    obj_w_sem = _obj + '[' + list_to_str(_obj_sem) + ']'
                    _triplet_w_sem = (sub_w_sem + "||" + _verb + "||" + obj_w_sem)
                    _triplet_wo_sem = (_sub + "||" + _verb + "||" + _obj)

                    triple_scores = (sim_sub_max_score + sim_verb_max_score + sim_obj_max_score) / 3
                    _triplets_w_sem_to_scores[_triplet_w_sem] = triple_scores
                    _triplets_wo_sem_to_scores[_triplet_wo_sem] = triple_scores

                if len(_triplets_wo_sem_to_scores) <= 2:
                    ##TODO reducing Duplicated
                    sent_triplet_wo_sem.append(list(_triplets_wo_sem_to_scores.keys()))

                else:
                    sent_triplet_wo_sem_sorted = sorted(_triplets_wo_sem_to_scores.items(), key=lambda x: -x[1])
                    triples_outputs = sent_triplet_wo_sem_sorted[:4]

                    _wo_svos = []
                    for output in triples_outputs:
                        _wo_svos.append(output[0])
                    sent_triplet_wo_sem.append(_wo_svos)

                if len(_triplets_w_sem_to_scores) <= 2:
                    sent_triplet_w_sem.append(list(_triplets_w_sem_to_scores.keys()))

                else:
                    sent_triplet_w_sem_sorted = sorted(_triplets_w_sem_to_scores.items(), key=lambda x: -x[1])
                    triples_outputs = sent_triplet_w_sem_sorted[:4]
                    _w_svos = []
                    for output in triples_outputs:
                        _w_svos.append(output[0])
                    sent_triplet_w_sem.append(_w_svos)

            para_triplets_w_sem.append(sent_triplet_w_sem)
            para_triplets_wo_sem.append(sent_triplet_wo_sem)
        all_svos_w_sem.append(para_triplets_w_sem)
        all_svos_wo_sem.append(para_triplets_wo_sem)

    return all_svos_wo_sem,all_svos_w_sem

def write_file(path, dt_ls):
    with open(path, 'w') as fw:
        for i, _para in enumerate(dt_ls):
            fw.write("Abstract " + str(i))
            fw.write("\n")
            for _sent in _para:
                for svos in _sent:
                    if len(svos) > 1:
                        for svo_ in svos:
                            fw.write(svo_)
                            fw.write("\t")

                    else:
                        res = ' '.join(svos)
                        fw.write(res)
                        fw.write("\t")

                fw.write("\n")
            fw.write("\n")

if __name__ == "__main__":

    all_Utttexts , all_phrase_w_semtypes = handleMMres('data/mmres_0817A.json')
    svo_wo_sem, svo_w_sem = getSVOs_w_sem_and_wo_sem(all_Utttexts, all_phrase_w_semtypes)

    write_file("data/final_wo_sem.txt", svo_wo_sem)
    write_file("data/final_w_sem.txt", svo_w_sem)

