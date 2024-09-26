class Agent(object):
    def __init__(self, phoneme_table, vocabulary) -> None:
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None

    def asr_corrector(self, environment):
        self.best_state = environment.init_state
        initial_cost = environment.compute_cost(environment.init_state)
        
        # Start with character-level corrections
        for i, char in enumerate(environment.init_state):
            if char in self.phoneme_table:
                for substitute in self.phoneme_table[char]:
                    new_state = (environment.init_state[:i] + substitute + environment.init_state[i+1:])
                    new_cost = environment.compute_cost(new_state)
                    if new_cost < initial_cost:
                        self.best_state = new_state
                        initial_cost = new_cost
                        print("doing character level of", i)
        # Next, try adding missing words at the start or end
        for word in self.vocabulary:
            for position in ['start', 'end']:
                if position == 'start':
                    new_state = word + " " + self.best_state
                else:
                    new_state = self.best_state + " " + word
                
                new_cost = environment.compute_cost(new_state)
                if new_cost < initial_cost:
                    self.best_state = new_state
                    initial_cost = new_cost
                    print("doing missing level of", word)
        # Implement additional search strategies as needed to refine the best state