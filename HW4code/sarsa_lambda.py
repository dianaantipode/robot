import numpy as np
import itertools

def sarsa_lambda(initial_Q,initial_state,transition,
          num_episodes,gamma, alpha, lambda_, epsilon=0.1):
    """
    This function implements backward view of Sarsa(lambda). It returns learned Q values.
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
        E = np.zeros([num_states,num_actions]) 
        state_visit = []
        ep_reward= 0 
        state = initial_state
        action = np.random.randint(0, 4)
        is_term = False
        
        while is_term == False:
            sprime, reward, is_term = transition(state,action)
            aprime = epsilon_greedy(Q[sprime], epsilon)
            delta = reward + gamma *  Q[sprime, aprime] - Q[state,action]
            E[state,action] = E[state,action] +1
            
            for state in range(num_states):
                for action in range(num_actions):
                    Q[state,action] += alpha * delta * E[state,action]
                    E[state,action] *= gamma*lambda_
            
            state_visit.append(state)
            ep_reward += reward
            
            state = sprime
            action = aprime
            
        rewards[ep] = ep_reward
        steps[ep] = len(state_visit)
       
            
    return Q,  steps, rewards
        
"""
   Initialize Q(s,a) for all states and actions (from states) check
   Repeat for each episode
       Eligibility trace: E(s,a) = 0 for all states and actions check
       Initialize s and a
       Repeat for each step of the episode
           take action A, observe R and sprime
           choose aprime  using policy derived from Q
           error = R + gamma* Q(sprime, aprime) - Q(s,a)
           E(s,a) = E(s,a) + 1
           for s in range num states :
               for all actions in actions:
                   Q(s,a) = Q(s,a) + alpha * error*E(s,a)
                   E(S,a) = gamma*lamdba*E(s,a)
          S = sprime
          a = aprime
   until S is terminal
   
"""   