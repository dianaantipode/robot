import numpy as np

#randomPolicy = np.ones([8,3]) / 2

initial_v = np.zeros(8)

def get_episode_Walk(policy):

    state = 0 # index of the initial state 
         
    states = [state]
    actions = []
    rewards = []
    state_count = 0 
    
    while state_count <=10:
        action = np.random.binomial(0,2)
        if action == 0: 
            next_state = state
        elif action == 1:
            next_state = np.random.ranint(state+1,8)
        else:
            next_state = np.random.ranint(0,state-1)
        
              
        states.append(next_state)
        actions.append(action)
        rewards.append(0)
        state = next_state
        state_count += 1
    
    