# Plane Boarding
Plane on boarding [OpenAI gym](https://github.com/openai/gym) environment simulator. This simulator has a 
__particularity__ to be taken into consideration when developing DRL algorithms for it, the interaction with the 
environment occurs just __once__ and __previous__ to the simulation. 

This is due to the _real world_ limitation of airlines, related to queue rearrangements. That means, that airlines have
no real-time information of the plane layout filling and passengers position at each time step. This would allow an
interactive _plane on boarding simulation_ , thus would prevent us from any implementation in the real world. As a
second factor, the gains on speed by an __all mighty__ queueing agent, would be strongly counterbalanced by people's
user experience, due to possible multiple queue rearrangements affecting the same passenger many times. 

## Spaces specifications
### State
State space consists basically of ```(row, column, baggage) * num_passengers```, this encapsulates the full description
of all the passengers known information.

### Action
The action space is basically an ordering for the passengers queue. This ordering is expected to be, a prioritization
assignation value of the queue; for the neural network agent training, a log-softmax approach will be take into the last 
layer, provoking that the passenger with higher priority to on board will be the one with the highest value, the second 
on priority to on board will be the second highest value and so on.

### Reward
Reward is negative,; the __less time the simulation spends the better__. As simulation is deterministic, the time spent is
 attributable to the queue ordering ability.

## Versions
Three different versions of the 

### Airbus  380
A plan on-boarding simulator environment for OpenAI gym; based on a Lufthansa's Airbus A380-800 (388) V1 configuration
(564 seats). Adapted to the current unique seat layout configuration. Having 57 seat rows (570 seats); 
564 seats / 10 seats per row = 56,4

- Seats: 570
- Row layout: (1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1); if 1 "seat" else "aisle"

```
env = gym.make('gym_plane_boarding:a380-v0')
```

### Boeing 737
A plan on-boarding simulator environment for OpenAI gym; based on a Lufthansa's Boeing 737-300 (737) configuration 
(124 seats). Adapted to the current unique seat layout configuration. Having 21 seat rows (126 seats);
124 seats / 6 seats per row = 20,667

- Seats: 126
- Row layout: (1, 1, 1, 0, 1, 1, 1); if 1 "seat" else "aisle"

```
env = gym.make('gym_plane_boarding:b737-v0')
```

### Boeing 747
A plan on-boarding simulator environment for OpenAI gym; based on a Lufthansa's Boeing 747-400 (744) V1 configuration
(393 seats). Adapted to the current unique seat layout configuration. Having 50 seat rows (400 seats);
 393 seats / 8 seats per row = 49,125
 
- Seats: 400
- Row layout: (1, 1, 0, 1, 1, 1, 1, 0, 1, 1); if 1 "seat" else "aisle"

 ```
env = gym.make('gym_plane_boarding:b747-v0')
```

# Installation
To install the environment on your [OpenAI gym](https://github.com/openai/gym) installation, please proceed as stated
under:
```bash
cd 19_project_plane_boarding/gym_plane_boarding
pip install -e .
```
