import argparse
from fsmgenerator.fsm import Fsm
from fsmgenerator.state import State
from fsmgenerator.transition import Transition
from fsmgenerator.net import Net
import random
import math


class Generator():
    def __init__( self ):
        self._parseArgumentsAndGenerate()

    def _parseArgumentsAndGenerate( self ):
        self._parseArguments()
        self._generate()

    def _parseArguments( self ):

        self._initArgumentParser()
        self._addArgumentStateCount()
        self._addArgumentTransitionCount()
        self._addArgumentSeed()
        self._addArgumentOutputDotFile()
        self._addArgumentInputWidth()
        self._addArgumentOutputWidth()
        self._addArgumentMaxNetLenght()
        self._addArgumentMinNetProbability()
        self._addArgumentIterations()
        self._addArgumentPythonOutput()
        self._addArgumentScl300Output()
        self._addArgumentScl1500Output()
        self._addArgumentDebug()

        self._args = self._parser.parse_args()

    def _initArgumentParser( self ):
        self._parser = argparse.ArgumentParser(
            prog = 'fsm_generator',
            description = 'Generates a randomized finite state machine with source code.')

    def _addArgumentStateCount( self ):
        self._parser.add_argument( '-c', '--state-count',
                type = int, required = True,
                help = 'Number of FSM states.' )

    def _addArgumentTransitionCount( self ):
        self._parser.add_argument( '-t', '--transition-count',
                type = int, required = True,
                help = 'Maximal number of transitions from one states.' )

    def _addArgumentSeed( self ):
        self._parser.add_argument( '-s', '--seed',
                type = int, default = 42,
                help = 'Random number generator seed.' )

    def _addArgumentOutputDotFile( self ):
        self._parser.add_argument( '--dot-file',
                type = str, default = 'fsm.dot',
                help = 'Output file for the FSM.dot description.' )

    def _addArgumentInputWidth( self ):
        self._parser.add_argument( '--input-width',
                type = int, default = 32,
                help = 'Width of the input network in bit.' )

    def _addArgumentOutputWidth( self ):
        self._parser.add_argument( '--output-width',
                type = int, default = 32,
                help = 'Width of the output network in bit.' )

    def _addArgumentMaxNetLenght( self ):
        self._parser.add_argument( '-l', '--max-net-length',
                type = int, default = 5,
                help = 'Maximal logic operations network length.' )

    def _addArgumentMinNetProbability( self ):
        self._parser.add_argument( '-m', '--min-net-prob',
                type = Generator.float_range( 0.01, 0.99 ), default = 0.1,
                help = 'Minimal net transition probability.' )

    def _addArgumentIterations( self ):
        self._parser.add_argument( '-i', '--iterations',
                type = str, default = 16 * 1024,
                help = 'Amount of input words in the input stimulus.' )

    def _addArgumentPythonOutput( self ):
        self._parser.add_argument( '--python-output',
                type = str,
                help = 'Output file for the python code generation.' )

    def _addArgumentScl300Output( self ):
        self._parser.add_argument( '--scl-300-output',
                type = str,
                help = 'Output file for the SCL 300 code generation.' )

    def _addArgumentScl1500Output( self ):
        self._parser.add_argument( '--scl-1500-output',
                type = str,
                help = 'Output file for the SCL 1500 code generation.' )

    def _addArgumentDebug( self ):
        self._parser.add_argument( '--demo',
                action = 'store_true',
                help = 'Generate intermediate .dot files of the FSM generation process.' )

    def _generate( self ):
        self._generateFsm()
        self._generateInputAndOutputNetworks()
        self._generateCode()

    def _generateFsm( self ):
        random.seed( self._args.seed )
        self._generateStates()
        self._addRandomFsmTransitions()
        self._addTransitionsToUnreachableStates()

        self._fsm.writeDotFile( self._args.dot_file )

    def _generateStates( self ):
        self._fsm = Fsm( self._args.state_count )
        self._fsm.writeDotFile( 'demo_states.dot' )

    def _addRandomFsmTransitions( self ):
        for state in self._fsm.getStateList():
            self._addRandomStateTransitions( state )
        self._fsm.updateReachability()
        if self._args.demo:
            self._fsm.writeDotFile( 'demo_random_transitions.dot' )

    def _addRandomStateTransitions( self, state : State ):
        count = random.randint( 1, self._args.transition_count )

        for j in range( count ):
            destination = random.choice( self._fsm.getStateList() )
            transition = Transition( state, destination )
            state.addTransition( transition )
            destination.addReachedBy( state )

    def _addTransitionsToUnreachableStates( self ):
        self._fsm.checkLocalReachability()

        for state in self._fsm.getStateList():
            if ( state.isReached() ):
                continue

            source = state.getNumber()
            while ( source == state.getNumber() ):
                source = random.randint( 0, self._args.state_count - 1 )

            sourceState = self._fsm.getState( source )
            transition = Transition( source, state, '#ff0000' )
            sourceState.addTransition( transition )

        self._fsm.updateReachability()
        if self._args.demo:
            self._fsm.writeDotFile( 'demo_locally_reachable.dot' )
        self._fsm.checkGlobalReachability()
        if self._args.dot_file:
            self._fsm.writeDotFile( self._args.dot_file )

    def _generateInputAndOutputNetworks( self ):
        self._generateInputNetwork()
        self._generateOutputNetwork()

    def _generateInputNetwork( self ):
        self._inputNetworkList = self._generateNetwork(
                self._args.input_width, 0, self._args.input_width )

    def _generateOutputNetwork( self ):
        self._outputNetworkList = self._generateNetwork(
                self._args.input_width, self._args.input_width,
                self._args.output_width )


    def _generateNetwork( self, firstInputWidth : int, secondInputWidth : int,
            outputWidth : int ) -> []:
        netList = []
        for q in range( outputWidth ):
            net = Net( q, firstInputWidth, secondInputWidth, self._args.min_net_prob )
            for i in range( random.randint( 1, self._args.max_net_length ) ):

                if ( not net.addInput() ): break

            netList.append( net )

        return netList

    def _generateCode( self ):
        self._randomizeInputAssignment()
        if self._args.python_output:
            self._generatePythonCode()
        if self._args.scl_300_output:
            self._generateScl300Code()
        if self._args.scl_1500_output:
            self._generateScl1500Code()

    def _randomizeInputAssignment( self ):
        for state in self._fsm.getStateList():
            transCount = state.getTransitionCount()
            inputWidth = int( math.ceil( math.log( transCount, 2 ) ) )
            inputStart = random.randint( inputWidth, self._args.input_width - 1 )
            state.setInputPart( inputStart, inputWidth )

    def _generatePythonCode( self ):
        code = open( self._args.python_output, 'w' )
        code.write( '#!/usr/bin/env python\n' )
        code.write( '\n' )

        x2 = ''

        if ( self._inputNetworkList[ 0 ]._X2_WIDTH > 0 ): x2 = ', x2'

        code.write( 'def inputNet( x1{} ):\n'.format( x2 ) )
        code.write( '\n' )
        code.write( '    q = 0\n' )

        for net in self._inputNetworkList:

            code.write( '    {}\n'.format( net.generatePython() ) )

        code.write( '    return q\n' )
        code.write( '\n' )

        x2 = ''

        if ( self._outputNetworkList[ 0 ]._X2_WIDTH > 0 ): x2 = ', x2'

        code.write( 'def outputNet( x1{} ):\n'.format( x2 ) )
        code.write( '\n' )
        code.write( '    q = 0\n' )

        for net in self._outputNetworkList:

            code.write( '    {}\n'.format( net.generatePython() ) )

        code.write( '    return q\n' )

        code.write( '\n' )
        code.write( 'def transition( e, q1 ):\n'.format( x2 ) )
        code.write( '\n' )
        code.write( '    q = 0\n' )
        code.write( '\n' )
        c = 'if'
        for state in self._fsm.getStateList():
            code.write( '    {} ( q1 == {} ):\n'.format( c, state.getNumber()) )
            state.generatePython( code )
            c = 'elif'

        code.write( '    return q\n' )

        code.write( '\n' )
        code.write( 'def lfsr14( seed ):\n' )
        code.write( '\n' )
        code.write( '    seed = seed * 2\n' )
        code.write( '    p    = ( ( seed >> 14 ) & 1 ) ^ ( ( seed >> 13 ) & 1 ) ^ ( ( seed >> 12 ) & 1 ) ^ ( ( seed >> 2 ) & 1 )\n' )
        code.write( '    seed = seed + p\n' )
        code.write( '    return seed & 0x3fff\n' )
        code.write( '\n' )
        code.write( 'def getRandomInput( seed ):\n' )
        code.write( '\n' )
        code.write( '    seed = lfsr14( seed )\n' )
        code.write( '    p1 = seed << 28\n' )
        code.write( '    p2 = seed << 14\n' )
        code.write( '    p3 = seed\n' )
        code.write( '    return p1 + p2 + p3\n' )
        code.write( '\n' )
        code.write( 'def controlLoop( size, seed ):\n' )
        code.write( '    q_t = 0\n' )
        code.write( '\n' )
        code.write( '    for i in range( size ):\n' )
        code.write( '        seed = getRandomInput( seed ) & 0xffffffff\n' )
        code.write( '        e    = inputNet( seed )\n' )
        code.write( '        q_t1 = transition( e, q_t )\n' )
        code.write( '        print( \'{}, {}->{}, {:08x}\'.format( q_t, q_t, q_t1, e ) )\n' )
        code.write( '        q_t  = q_t1\n' )
        code.write( '\n' )
        code.write( 'size = {}\n'.format( self._args.iterations ) )
        code.write( 'seed = {}\n'.format( 42 ) )
        code.write( '\n' )
        code.write( 'print( \'state, transition, input\' )\n' )
        code.write( '\n' )
        code.write( 'controlLoop( size, seed )\n' )

    @staticmethod
    def float_range( minimum : float, maximum : float ):
        def float_range_checker(arg):
            try:
                f = float( arg )
            except ValueError:
                raise argparse.ArgumentTypeError(
                        'must be a floating point number' )

            if f < minimum or f > maximum:
                raise argparse.ArgumentTypeError(
                        'must be in range [{:f} .. {:f}}'.format( minimum, maximum ) )
            return f

        return float_range_checker


