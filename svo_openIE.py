from openie import StanfordOpenIE

properties = {
    'openie.affinity_probability_cap': 1.0,
    'CorefChainAnnotation.resolve_coref':True,
    'openie.triple.strict': True,
    "openie.max_entailments_per_clause":150,
    "openie.threads":10
}
client = StanfordOpenIE(install_dir_path='4.1.0')


def getSVOs(sentence):
    triple_res_list = []
    triples = client.annotate(sentence, properties=properties)
    for triple in triples:
        sub_ = triple['subject']
        obj_ = triple['object']
        rel_ = triple['relation']
        triple_res_list.append((sub_,rel_,obj_))
    return triple_res_list


# if __name__ == "__main__":
#     text = "Tom likes dogs, and dogs are important for his life."
#     res = getSVOs(text)
#     for triple in res:
#         print(triple)
#     # print(res)