from pykleene.nfa import NFA
from typing import Dict
from config import INPUTPATH, OUTPUTDIR
import json

FILENAME = 'nfas.json'

if __name__ == '__main__':
    NFAs: Dict[str, NFA]
    with open(INPUTPATH(FILENAME), 'r') as file:
        NFAs = json.load(file)

    for nfaName, nfaData in NFAs.items():
        dfa = NFA()
        dfa.loadFromJSONDict(nfaData)
        dfa.image(dir=OUTPUTDIR(), save=True)
        NFAs[nfaName] = dfa

    for nfaName, nfa in NFAs.items():
        nfa.image(dir=OUTPUTDIR(), save=True)
        regex = nfa.regex()
        print(f"Regex for {nfaName}: {regex}")
        