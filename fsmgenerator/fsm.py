from fsmgenerator.state import State
from fsmgenerator.transition import Transition
import random

class Fsm:
    def __init__( self, stateCount ):

        self._stateCount = stateCount
        self._stateList  = []

        for i in range( self._stateCount ):
            self.addState( State( i ) )

    def addState( self, state ):
        self._stateList.append( state )

    def getStateList( self ):
        return self._stateList

    def getState( self, number ):
        return self.getStateList()[ number ]


    def updateReachability( self ):
        for state in self._stateList:
            state.updateReachability( [] )

    def checkLocalReachability( self ):
        for state in self._stateList:
            for transition in state.getTransitionList():
                index = transition.getDestination().getNumber()
                destination = self._stateList[ index ]
                destination.addReachedByList( state.getReachedByList() )

    def checkGlobalReachability( self ):
        for source in self._stateList:
            for destination in self._stateList:
                if ( source.reaches( destination ) ):
                    continue

                randomState = random.choice( list( source.getReachesList() ) )
                transition = Transition( randomState, destination, '#00ff00' )
                randomState.addTransition( transition )
                randomState.addReachesList( destination.getReachesList() )
                self.updateReachability()

    def writeDotFile( self, fileName ):
        dotFile = open( fileName, 'w' )
        dotFile.write( 'digraph G1 {\n' )
        dotFile.write( '  RESET [ style = invisible ];\n' )

        for state in self.getStateList():
            dotFile.write( '  {};\n'.format( state.getName() ) )

        dotFile.write( '\n' )
        dotFile.write( '  RESET -> N0 [ label = " reset" ];\n' )
        dotFile.write( '\n' )

        for state in self.getStateList():
            for transition in state.getUniqueTransitionList():
                dotFile.write( \
                    '  {} -> {} [ color = "{}" ];\n'.format( \
                        state.getName(),
                        transition.getDestinationName(),
                        transition.getColor() ) )

        dotFile.write( '}\n' )

