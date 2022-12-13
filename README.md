# fsm_generator
A randomized finite state machine generator.

# Generation Process

The generation is seperated in two parts.
At first the FSM and its transitions is generated.
In the second optional part a source code implementing the generated FSM is
created.

## FSM Generation Process

At first the generator creates the selected amount of state objects.
Each state node is named with an upper case 'N' followed by the states number.
The second generation step iterates over all states of the FSM and adds a
random amount of transitions between 1 and **--transition_count** to each state.
The target of each transition is a random state of the FSM.
The following state machine is generated with this two steps if the demo
parameters of five states and between one and three transitions
per state are applied.

![First Generation Step](/doc/demo_random_transitions.jpg?raw=true)

The third generation step ensures that each state is reachable by at least one
other state.
If this is not the case a random state (not the unreachable) is chosen and an
additional transition is added from the chosen state to the unreachable state.
After this generation step the red colored transitions are added to the demo
FSM.

![Second Generation Step](/doc/demo_locally_reachable.jpg?raw=true)

In a final step the generator checks the global reachability of each state.
There must be a path from each state to every other state.
If one state is not reachable by another, one of the reachable states is
randomly chosen and a transition is added from the chosen state to the
unreachable state.
This leads to the final FSM graph shown in the figure below.
The transitions added in the final generation step are highlighted in green.

![Third Generation Step](/doc/demo.jpg?raw=true)

## Source Code Generation Process

The generated FSM source code consists of the following three steps:

1. A LSFR based random input value generation
2. The boolean logic based input network
3. The CASE and IF-ELSE based state transition

The LFSR is used to avoid target dependent random number generation and to get
deterministic random numbers.

The boolean logic input networks consist of AND, OR, XOR and NOT operations
that concatenate randomly chosen bits of the input word.

The CASE and IF-ELSE based state transition takes the possible transitions of
the current state and creates an equal distribution based selection of the next
state.

With the demo creation parameters the python-code (--python-output) state
machine performs the following first 100 state transitions.

![Third Generation Step](/doc/iterations.jpg?raw=true)

