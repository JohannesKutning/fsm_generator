# fsm_generator
A randomized finite state machine generator.

# Generation Process

At first the generator creats the selected amount of state objects.
Each state node is named with an upper case 'N' followed by the states number.
The second generation step iterates over all states of the FSM and adds a
random amount of transitions between 1 and **--transition_count** to each state.
The target of each transition is a random state of the FSM.
The following state machine is generated with this two steps if the demo
paramters of five states and between one and three transitions
per state are applied.

