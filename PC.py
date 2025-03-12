import random

class PC:
    def __init__(self, initial_pillars, max_blocks_per_turn):
        self.initial_pillars = initial_pillars
        self.max_blocks_per_turn = max_blocks_per_turn
        self.pillars = initial_pillars.copy()
        self.winner = None
        self.player = 0  # 0 for player 1, 1 for AI
        self.q_table = {}  

    def available_actions(self, state):
        actions = set()
        for i in range(len(state)): # All possible moves for loop
            for j in range(1, min(state[i], self.max_blocks_per_turn) + 1):
                actions.add((i, j)) 
        return actions
    
    def find_q_value(self, state, action):
        return self.q_table.get((tuple(state), action), 0)

    def best_future_reward(self, state):
        best_reward = 0
        for action in self.available_actions(state):
            reward = self.find_q_value(state, action)
            if reward > best_reward:
                best_reward = reward
        return best_reward

    def update_q(self, old_state, action, new_state, reward, alpha):
        old_q = self.find_q_value(old_state, action)
        best_reward = self.best_future_reward(new_state)
        self.q_table[(tuple(old_state), action)] = old_q + alpha * (reward + best_reward - old_q)

    def choose_best_action(self, state, epsilon):
        all_actions = self.available_actions(state)
        best_action = None
        best_reward = 0

        for action in all_actions:
            reward = self.find_q_value(state, action)
            if best_action is None or reward > best_reward:
                best_action = action
                best_reward = reward

        weights = [epsilon] * len(all_actions)
        if best_action:
            weights[list(all_actions).index(best_action)] = 1 - epsilon
        best_action = random.choices(list(all_actions), weights, k=1)[0]

        return best_action


    def move(self, action):
        pile, count = action

        if count > self.max_blocks_per_turn:
            raise Exception("Exceeded maximum blocks allowed per turn")
        elif pile < 0 or pile >= len(self.pillars):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.pillars[pile]:
            raise Exception("Invalid number of objects")

        self.pillars[pile] -= count
        if all(pile == 0 for pile in self.pillars):
            self.winner = 1 - self.player  
        else:
            self.player = 1 - self.player


    def train(self, n):
        epsilon = 0.1
        alpha = 0.5
        
        for i in range(n):
            self.pillars = self.initial_pillars.copy()
            self.player = 0
            self.winner = None

            last = {
                0: {"state": None, "action": None},
                1: {"state": None, "action": None}
            }

            while True:
                state = self.pillars.copy()
                best_action = self.choose_best_action(state, epsilon)

                if best_action is None:
                    break

                last[self.player]["state"] = state
                last[self.player]["action"] = best_action

                self.move(best_action)
                new_state = self.pillars.copy()

                if self.winner is not None:
                    self.update_q(state, best_action, new_state, -1, alpha)
                    self.update_q(last[1 - self.player]["state"], last[1 - self.player]["action"], new_state, 1, alpha)
                    break
                elif last[self.player]["state"] is not None:
                    self.update_q(last[self.player]["state"], last[self.player]["action"], new_state, 0, alpha)


