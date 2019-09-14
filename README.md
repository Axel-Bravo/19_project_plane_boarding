# On boarding
Project aimed at developing a Open Gym AI environment focused on the on boarding problem of planes. The project has
been focused in the realization of:

1. Creation of a Gym environment, can be found under: `\gym_plane_boarding\` 
2. Creation of a simple DRL algorithm to start solving the challenge, by using `Deep Q-learning`
3. Creation of more advanced DRL algorithms

## Structure 
There are two developments:
- The gym environment, for more information see its own README in: `\gym_plane_boarding\` 
- The development of the DRL Deep-Q Network algorithm, in the source folder: `\src\` 
 

On the source folder there are mainly two developments:
- `plane_boarding_simulator`: contains a self-contained plane boarding simulator, in which the gym environment is based

- `plane_boarding` + `utils`: contains the Deep-Q Network implementation (not completed, see _Problematic_). 

## Problematic 
Though being aware of the difficulty in the training fo the simulator, as the simulator has only one action per
execution, for more information see the README from the environment. `gym_plane_boarding\README.md`. 

It was decided to take it as a __challenge__, as this was my first _gym environment_ implementation. And to try to 
adapt the __Deep-Q Network__ algorithm to the new _Tensorflow 2.0 (RC)_ library. 

The main problem comes from the own __Deep-Q Network__ algorithm: 

    # Get max predicted Q values (for next states) from target model
    Q_targets_next = self.qnetwork_target(next_states).detach().max(1)[0].unsqueeze(1)
    
    # Compute Q targets for current states 
    Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))

    # Get expected Q values from local model
    Q_expected = self.qnetwork_local(states).gather(1, actions)

    # Compute loss
    loss = F.mse_loss(Q_expected, Q_targets)
    # Minimize the loss
    self.optimizer.zero_grad()
    loss.backward()
     self.optimizer.step()

The below algorithm shows how we need to have _incremental_ steps in order for the algorithm to properly learn, this is 
_something we __cannot guarantee__ with the current gym implementation_. This is a step at the moment __it is not seen
how to easily solve__. 

For this reason, at the moment, the repository will be *held as __archived__*. 
