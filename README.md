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

![First Generation Step](/doc/demo_random_transitions.jpg?raw=true)

The third generation step ensures that each state is reachable by at least one
other state.
If this is not the case a random state (not the unreachable) is choosen and an
additional transition is added from the choosen state to the unreachable state.
After this generation step the red colored transisions are added to the demo
FSM.

![Second Generation Step](/doc/demo_locally_reachable.jpg?raw=true)

In a final step the generator checks the global reachablility of each state.
There must be a path from each state to every other state.
If one state is not reachable by another, one of the reachable states is
randomly choosen and a transition is added from the choosen state to the
unreachable state.
This leads to the final FSM graph shown in the figrue below.
The transitions added in the final gernation step are highlighted in green.

![Third Generation Step](/doc/demo.jpg?raw=true)
