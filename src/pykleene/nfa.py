class NFA:
    states: set[str]
    alphabet: set[str]
    transitions: dict[tuple[str, str], set[str]]
    startStates: set[str]
    finalStates: set[str]

    def __init__(self, 
                 states: set[str] = set(), 
                 alphabet: set[str] = set(), 
                 transitions: dict[tuple[str, str], set[str]] = dict(), 
                 startStates: set[str] = set(), 
                 finalStates: set[str] = set()):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.startStates = startStates
        self.finalStates = finalStates

    def loadFromJSONDict(self, data: dict):
        self.states = set(data['states'])
        self.alphabet = set(data['alphabet'])
        self.transitions = dict()
        for transition in data['transitions']:
            self.transitions[(transition[0], transition[1])] = set(transition[2])
        self.startStates = set(data['startStates'])
        self.finalStates = set(data['finalStates'])

    def _addTransition(self, startState: str, symbol: str, endState: str) -> 'NFA':
        for (state, sym), nextStates in self.transitions.items():
            if state == startState and sym == symbol:
                nextStates.add(endState)
                return self
        self.transitions[(startState, symbol)] = {endState}
        return self

    def singleStartStateNFA(self) -> 'NFA':
        from copy import deepcopy
        newNfa = deepcopy(self)
        cnt = 0
        while f"q{cnt}" in newNfa.states:
            cnt += 1
        newStartState = f"q{cnt}"
        newNfa.states.add(newStartState)
        for startState in newNfa.startStates:
            newNfa.transitions[(newStartState, 'ε')] = {startState}
        newNfa.startStates = {newStartState}
        return newNfa


    def singleFinalStateNFA(self) -> 'NFA':
        from copy import deepcopy
        newNfa = deepcopy(self)
        cnt = 0
        while f"q{cnt}" in newNfa.states:
            cnt += 1
        newFinalState = f"q{cnt}"
        newNfa.states.add(newFinalState)
        for finalState in newNfa.finalStates:
            newNfa.transitions[(finalState, 'ε')] = {newFinalState}
        newNfa.finalStates = {newFinalState}
        return newNfa 

    def regex(self) -> str:
        nfa = self.singleStartStateNFA().singleFinalStateNFA()

        def R(startState: str, states: set[str], finalState: str) -> str:
            if len(states) == 0:
                alphabet = set()
                for (state, symbol), nextStates in nfa.transitions.items():
                    if state == startState and finalState in nextStates:
                        alphabet.add(symbol) 
                if startState != finalState:
                    if len(alphabet) == 0:
                        return 'φ'
                    else:
                        return '+'.join(alphabet)
                if startState == finalState:
                    if 'ε' not in alphabet:
                        alphabet.add('ε')
                    return '+'.join(alphabet)
            else:
                r = states.pop()
                X = states
                return f"(({R(startState, X, finalState)})+({R(startState, X, r)})({R(r, X, r)})*({R(r, X, finalState)}))"

    def reverse(self) -> 'NFA':
        reversedNfa = NFA(
            states=self.states,
            alphabet=self.alphabet,
            transitions=dict(),
            startStates=self.finalStates,
            finalStates=self.startStates
        )
        transMap: dict[tuple[str, str], set[str]] = dict()
        for (state, symbol), nextStates in self.transitions.items():
            for nextState in nextStates:
                if (nextState, symbol) not in transMap:
                    transMap[(nextState, symbol)] = set()
                if state not in transMap[(nextState, symbol)]:
                    transMap[(nextState, symbol)].add(state)
        reversedNfa.transitions = transMap
        return reversedNfa
            