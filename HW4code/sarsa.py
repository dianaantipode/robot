import numpy as np

def sarsa(initial_Q,initial_state,transition,
          num_episodes,gamma, alpha, epsilon=0.1):
    """
    This function implements Sarsa. It returns learned Q values.
    To crete Figure 6.3 and 6.4, the function also returns number of steps, and 
    the total rewards in each episode.
        
    Notes on inputs:    
    -transition: function. It takes current state s and action a as parameters 
                and returns next state s', immediate reward R, and a boolean 
                variable indicating whether s' is a terminal state. 
                (See windy_setup as an example)
    -epsilon: exploration rate as in epsilon-greedy policy

    """  
    def epsilon_greedy(q, epsilon):
        act = q.size
        if np.random.rand() < epsilon:
            return np.random.randint(act)
        else:
            return np.argmax(q)
    
    # initialization    
    Q = np.copy(initial_Q)
    num_states, num_actions = Q.shape  
    
       
    steps = np.zeros(num_episodes,dtype=int) # store #steps in each episode
    rewards = np.zeros(num_episodes) # store total rewards for each episode
    
    for ep in range(num_episodes):
        s = initial_state
        a = epsilon_greedy(initial_Q, epsilon) 
        state_visit = []
        ep_reward= 0 
        is_term = False
        
        while is_term == False:
            sprime, reward, is_term = transition(s,a)
            aprime = epsilon_greedy(Q[sprime], epsilon)
            delta = reward + gamma *  Q[sprime, aprime] - Q[s,a]
            
            Q[s,a] += alpha * delta 
            
            state_visit.append(s)
            ep_reward += reward
            
            s = sprime
            a = aprime
            
        rewards[ep] = ep_reward
        steps[ep] = len(state_visit)
        
    return Q,  steps, rewards
        
"""
optimal route:
state: [0, 3]   action: right
state: [1, 3]   action: right
state: [2, 3]   action: right
state: [3, 3]   action: right
state: [4, 4]   action: right
state: [5, 5]   action: right
state: [6, 6]   action: right
state: [7, 6]   action: right
state: [8, 6]   action: right
state: [9, 6]   action: down
state: [9, 5]   action: down
state: [9, 4]   action: down
state: [9, 3]   action: down
state: [9, 2]   action: left
state: [8, 2]   action: left
state: [7,3]
number of steps:  15
"""