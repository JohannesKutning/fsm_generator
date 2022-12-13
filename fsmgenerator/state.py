from fsmgenerator.transition import Transition

class State:

    def __init__( self, number ):

        self._number         = number
        self._transitionList = []
        self._reachedByList  = set()
        self._reachesList    = set()
        self._inputStart     = 0
        self._inputWidth     = 0

    # end __init__

    def getNumber( self ) -> int:
        return self._number

    def getName( self ) -> str:
        return 'N{}'.format( self.getNumber() )

    def addTransition( self, transition : Transition ):
        self._transitionList.append( transition )
        self._reachesList.add( transition.getDestination() )

    def getTransitionList( self ) -> [ Transition ]:
        return self._transitionList

    def getUniqueTransitionList( self ):
        transitionList = []
        destinationList = []
        for transition in self.getTransitionList():
            destination = transition.getDestination().getNumber()
            if destination in destinationList:
                continue
            destinationList += [destination]
            transitionList += [transition]
        return transitionList

    def getTransitionCount( self ):
        return len( self.getTransitionList() )

    def addReachedBy    ( self, source ):
        self._reachedByList.add   ( source )

    def addReachedByList( self, source ):
        self._reachedByList.update( source )

    def getReachedByList( self ):
        return self._reachedByList

    def isReached       ( self ):
        return len( self._reachedByList ) > 0

    def addReaches( self, destination ):
        self._reachesList.append( destination )

    def addReachesList( self, destination ):
        self._reachesList.update( destination )

    def getReachesList( self ):
        return self._reachesList

    def reaches( self, destination ):
        return destination in self._reachesList

    def getReachesString( self ):

        s = '{:5s} reaches'.format( self.getName() )

        for reached in self.getReachesList():

            s += ' {:5s}'.format( reached.getName() )

        return s

    def updateReachability( self, path = [] ):

        reachability = self.getReachesList()

        if ( self.getName() in path ):
            return reachability

        path.append( self.getName() )
        for transition in self._transitionList:
            r = transition.getDestination().updateReachability( path )
            reachability.update( transition.getDestination().updateReachability( path ) )

        self._reachesList.update( reachability )

        return reachability

    def setInputPart( self, start, width ):
        self._inputStart = start
        self._inputWidth = width

    def generatePython( self, code ):
        if ( len( self.getTransitionList() ) == 1 ):
            code.write( '        q = {}\n'.format( self.getTransitionList()[ 0 ].getDestination().getNumber() ) )

        else:
            code.write( '        i = ( ( e >> {} ) & {} )\n'.format( self._inputStart, 2 ** self._inputWidth - 1 ) )
            c = 'if'

            for i in range( len( self.getTransitionList() ) ):
                transition = self.getTransitionList()[ i ]
                code.write( '        {} ( i == {} ):\n'.format( c, i ) )
                code.write( '            q = {}\n'.format( transition.getDestination().getNumber() ) )
                c = 'elif'

    def generateScl( self, code ):

        if ( len( self.getTransitionList() ) == 1 ):

            code.write( '\n' )
            code.write( '        #q1 := {};\n'.format( self.getTransitionList()[ 0 ].getDestination().getNumber() ) )
            code.write( '\n' )

        else:

            # extract the input signals
            code.write( '\n' )
            code.write( '        #i := SHR( IN := e, N := {} ) and {};\n'.format( self._inputStart, self._inputWidth ) )
            code.write( '\n' )

            c = 'if'

            for i in range( len( self.getTransitionList() ) ):

                transition = self.getTransitionList()[ i ]

                code.write( '        {} ( #i = {} ) then\n'.format( c, i ) )
                code.write( '\n' )
                code.write( '            #q1 := {};\n'.format( transition.getDestination().getNumber() ) )
                code.write( '\n' )

                c = 'elsif'

            code.write( '        end_if;\n' )
            code.write( '\n' )
