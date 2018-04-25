import numpy as np

def TD0(get_episode,policy, initial_v, gamma, alpha,num_episodes = 1):
# This function implements TD(0).
# get_episode: function to generate an episode
# policy: the policy to be evaluated 
# initial_v: initial estimate for value function v
# gamma: discount factor
# alpha: learning rate
# num_episodes: number of episodes (iterations)
# The function returns the estimate of v

    # initialization  
    v = np.copy(initial_v)
    
    for ep in range(num_episodes):
        states,_,rewards = get_episode(policy)
        T = len(rewards)
        
        for t in range(T):
            
            s = states[t]
            s_next = states[t+1]
            td_target = rewards[t] + gamma* v[s_next]
            td_delta = td_target - v[s]
            v[s] += alpha*td_delta
            #v[s] += v[s] + alpha*((rewards[s] + gamma* v[s_next]) - v[s])

    
    """
    
    """
    
    return v



def TD_n(get_episode, policy, initial_v, n, gamma, alpha,num_episodes = 1):
# This function implements n-step TD.
# get_episode: function to generate an episode
# policy: the policy to be evaluated 
# initial_v: initial estimate for value function v
# n: number of steps to look ahead
# gamma: discount factor
# alpha: learning rate
# num_episodes: number of episodes (iterations)
# The function returns the estimate of v

    def TD_G(rewards, gamma):
        total = 0
        for i in range(len(rewards)):
            total += pow(gamma, i)*rewards[i]
        return total

    # initialization
    v = np.copy(initial_v)
    
    for ep in range(num_episodes):
        states,_,rewards = get_episode(policy)
        # Iterate over the states (omit the last state)
        for i, state in enumerate(states):
            if i + n < len(states):
                g = TD_G(rewards[i:i+n], gamma)
                g += pow(gamma, n) * v[states[i + n]]
            else:
                g = TD_G(rewards[i:], gamma)
            v[state] += alpha * (g - v[state])
    return v



def TD_lambda(get_episode, policy, initial_v, lambda_, gamma, alpha,
              num_episodes=1):
# This function implements n-step TD.
# get_episode: function to generate an episode
# policy: the policy to be evaluated 
# initial_v: initial estimate for value function v
# lambda_: value of lambda in TD(lambda)
# gamma: discount factor
# alpha: learning rate
# num_episodes: number of episodes (iterations)
# The function returns the estimate of v
              
    # initialization 
    v = np.copy(initial_v)
     
    for ep in range(num_episodes):
        states, _, rewards = get_episode(policy)
        T = len(rewards)
        E = np.zeros(len(v))
        
        for t in range(T):
            s = states[t]
            s_next = states[t+1]
            delta = rewards[t] + gamma * v[s_next] - v[s]
            E *=gamma*lambda_ 
            E[s] += 1
            v += alpha * delta * E


    return v


        
