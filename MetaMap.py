## Metamap_V3

import subprocess
import json




def get_metamap_output(sentence):
    '''
    Given a sentence return the metamap best matching result (score, ID, term)
    sentence: str

    '''
    p = subprocess.Popen(f"echo {str(sentence)} | /home/xinghaowu/MasterThesis/MT_new_2022_06/UMLS/public_mm/bin/metamap20 --JSONn -I ", stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    output = str(output, 'utf-8')

    output = output.split('\n')

    # no mapped entities
    if len(output) < 2:
        return None
    try:
        output = json.loads(output[1])
        # output = process_output(output)
        return output
        # JSON Decoder
    except:
        return None

