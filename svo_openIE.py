from openie import StanfordOpenIE

properties = {
    'openie.affinity_probability_cap': 1.0,
    'CorefChainAnnotation.resolve_coref':True,
    'openie.triple.strict': True,
    "openie.max_entailments_per_clause":150,
    "openie.threads":10
}
client = StanfordOpenIE(install_dir_path='4.4.0')


def getSVOs(sentence):
    triple_res = client.annotate(sentence,properties=properties)
    return triple_res
