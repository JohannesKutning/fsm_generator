
class Transition:

    def __init__( self, source, destination, color = '#000000' ):

        self._source      = source
        self._destination = destination
        self._color       = color

    # end __init__

    def getSource( self ):
        return self._source

    def getDestination( self ):
        return self._destination

    def getDestinationName( self ):
        return 'N{}'.format( self._destination.getNumber() )

    def getColor( self ):
        return self._color

    def toString( self ):
        return '{} -> {}'.format( self._source.getName(), self._destination.getName() )
