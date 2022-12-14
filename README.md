# fsm_generator
A randomized finite state machine generator.

# Usage

Generates a FSM with five states and one or two randomized transitions
and writes the result into fsm.dot.


    fsm_generator -c 5 -t 2 --dot-file fsm.dot


You can view the entire command arguments by running.


    fsm_generator --help


## Additional FSM Generation Arguments

Set the randomization seed to get different creation results for the same set
of parameters.


    --seed SEED


To see the intermediate steps of the FSM generation the demo mode can be
enabled.
This leads to the generation of .dot files of all FSM generation steps
described in [FSM Generation Process](#FSM Generation Process).


    --demo


## Code Generation Arguments

The width of the input network defines the amount of input vector bits, that
are used to generate the boolean logic input network.
Additionally it defines the width of the integer input stimuli for each
iteration.


    --input-width INPUT_WIDTH


The width of the output network defines the amount of output vector bits, that
are used to generate the boolean logic output network.


    --output-width OUTPUT_WIDTH


The maximal network length defines the maximal boolean logic operations used in
each path of the input and output networks.


    -l MAX_NET_LENGTH / --max-net-lenght MAX_NET_LENGTH


The minimal network probability sets the lower limit of each input and
output network to produce a logical HIGH result.
This parameter is used the ensure an impact of each network on the state
transitions.
The value is limited to the range of [0.01, 0.99].


    -m MIN_NET_PROB / --min-net-prob MIN_NET_PROB


Set the amount of iterations of the input stimulus.


    -i ITERATIONS / --iterations ITERATIONS


To activate the python code generation a output file must be given to the
generator.
The generator writes python3 compatible code to the given source file.


    --python-output PYTHON_OUTPUT


To activate the SCL code generation for S7-1500 and/or S7-300 a output file
must be given to the generator with on or both of the following arguments.


    --scl-300-output SCL_300_OUTPUT
    --scl-1500-output SCL_1500_OUTPUT


# Demo Generation

There is a demo generation with the parameters used to generate the figures of
this README.
It is located in the **demo** folder and can be executed within this folder by
running:


    make


All generated demo files can be deleted by running:


    make clean


# Generation Process

The generation is separated in two parts.
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

