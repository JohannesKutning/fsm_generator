import random

class Net:

    def __init__( self, index, X1_WIDTH, X2_WIDTH, MIN_NET_PROB ):

        self._index         = index
        self._X1_WIDTH      = X1_WIDTH
        self._X2_WIDTH      = X2_WIDTH
        self._MIN_NET_PROB  = MIN_NET_PROB
        self._negationList  = []
        self._inputList     = []
        self._operationList = []
        self._prob          = 0.5

        # add the first input to net
        x = random.randint( 0, self._X1_WIDTH + self._X2_WIDTH - 1 )

        self._inputList.append( x )

        self._negationList.append( random.choice( [ True, False ] ) )

    def addInput( self ):

        x    = random.randint( 0, self._X1_WIDTH + self._X2_WIDTH - 1 )

        n    = random.choice( [ True, False ] )

        o    = random.choice( self._OPERATOR_LIST )

        prob = self._getOperationProbability( o )

        if ( prob < self._MIN_NET_PROB ): return False

        self._inputList.append( x )
        self._negationList.append( n )
        self._operationList.append( o )

        self._prob = prob

        return True

    def getProbability( self ): return self._prob

    def generatePython( self ):

        n = ''

        if ( self._negationList[ 0 ] ): n = '~ '

        index = self._inputList[ 0 ]

        x     = 'x1'

        if   ( index >= self._X1_WIDTH ):
            x      = 'x2'
            index -= self._X1_WIDTH

        x     = '( ( {} >> {} ) & 1 )'.format( x, index )

        s = 'q |= ( ( {}{}'.format( n, x )

        for i in range( len( self._operationList ) ):

            n = ''

            if ( self._negationList[ i + 1 ] ): n = ' ~ '

            index = self._inputList[ i + 1 ]

            x     = 'x1'

            if   ( index >= self._X1_WIDTH ):
                index -= self._X1_WIDTH
                x      = 'x2'

            x     = ' ( ( {} >> {} ) & 1 )'.format( x, index )

            o = self._toPythonOperator( self._operationList[ i ] )

            s += ' {}{}{}'.format( o, n, x )

        s += ' ) & 1 ) << {}'.format( self._index )

        return s

    def generateScl( self, version ):

        if   ( version == SCL_S7_300 ):  return self.generateScl300()
        elif ( version == SCL_S7_1500 ): return self.generateScl1500()

    def generateScl300( self ):

        n = ''

        if ( self._negationList[ 0 ] ): n = 'not '

        index = self._inputList[ 0 ]

        x1 = '#x1b_i'
        x2 = '#x2b_i'

        x  = x1

        if   ( index >= self._X1_WIDTH ):
            index -= self._X1_WIDTH
            x      = '#x2b_i'

        x     = '{}[ {} ]'.format( x, 31 - index )

        s = '#yb_i[ {} ] := {}{}'.format( 31 - self._index, n, x )

        for i in range( len( self._operationList ) ):

            n = ''

            if ( self._negationList[ i + 1 ] ): n = ' not '

            index = self._inputList[ i + 1 ]

            x  = x1

            if   ( index >= self._X1_WIDTH ):
                index -= 32
                x      = x2

            x     = ' {}[ {} ]'.format( x, 31 - index )

            o = self._operationList[ i ]

            s += ' {}{}{}'.format( o, n, x )

        s += ';'

        return s

    def generateScl1500( self ):

        n = ''

        if ( self._negationList[ 0 ] ): n = 'not '

        index = self._inputList[ 0 ]

        x1 = '#x1.%X'
        x2 = '#x2.%X'


        x  = x1

        if   ( index >= self._X1_WIDTH ):
            index -= self._X1_WIDTH
            x      = x2

        x     = '{}{}'.format( x, 31 - index )

        s = '#y.%X{} := {}{}'.format( 31 - self._index, n, x )

        for i in range( len( self._operationList ) ):

            n = ''

            if ( self._negationList[ i + 1 ] ): n = ' not '

            index = self._inputList[ i + 1 ]

            x  = x1

            if   ( index >= self._X1_WIDTH ):
                index -= 32
                x      = x2


            x     = ' {}{}'.format( x, 31 - index )

            o = self._operationList[ i ]

            s += ' {}{}{}'.format( o, n, x )

        s += ';'

        return s

    def toString( self ):

        n = ''

        if ( self._negationList[ 0 ] ): n = 'not '

        x = self._inputList[ 0 ]

        if   ( x < self._X1_WIDTH ): x = 'x1[ {} ]'.format( x )
        else: x = 'x2[ {} ]'.format( x )

        s = '{}{}'.format( n, x )

        for i in range( len( self._operationList ) ):

            n = ' '

            if ( self._negationList[ i + 1 ] ): n = ' not '

            x = self._inputList[ i + 1 ]

            if   ( x < self._X1_WIDTH ): x = 'x1[ {} ]'.format( x )
            else: x = 'x2[ {} ]'.format( x )

            o = self._operationList[ i ]

            s += ' {}{}{}'.format( o, n, x )

        return s

    def _getOperationProbability( self, o ):

        prob = 0.0

        if   ( o == 'and' ): prob = self._prob * 0.5
        elif ( o == 'or'  ): prob = self._prob + 0.5
        elif ( o == 'xor' ): prob = ( self._prob * 0.5 ) + ( ( 1 - self._prob ) * 0.5 )

        return prob

    def _toPythonOperator( self, o ): return self._PYTHON_OPERATOR_LIST[ self._OPERATOR_LIST.index( o ) ]

    _OPERATOR_LIST        = [ 'and', 'or', 'xor' ]
    _PYTHON_OPERATOR_LIST = [ '&', '|', '^' ]


def generateNetList( X1_WIDTH, X2_WIDTH, OUTPUT_WIDTH, MAX_NET_LENGTH, MIN_NET_PROB ):

    netList = []

    for q in range( OUTPUT_WIDTH ):

        net = Net( q, X1_WIDTH, X2_WIDTH, MIN_NET_PROB )

        for i in range( random.randint( 1, MAX_NET_LENGTH ) ):

            if ( not net.addInput() ): break

        netList.append( net )

    return netList


def generatePython( fsm, inputNetList, outputNetList, ITERATIONS ):

    code = open( 'fsm.py', 'w' )
    code.write( '#!/usr/bin/env python\n' )
    code.write( '\n' )
    code.write( 'import os\n' )
    code.write( 'import random\n' )
    code.write( 'import math\n' )
    code.write( '\n' )

    x2 = ''

    if ( inputNetList[ 0 ]._X2_WIDTH > 0 ): x2 = ', x2'

    code.write( 'def inputNet( x1{} ):\n'.format( x2 ) )
    code.write( '\n' )
    code.write( '    q = 0\n' )

    for net in inputNetList:

        code.write( '    {}\n'.format( net.generatePython() ) )

    code.write( '    return q\n' )
    code.write( '\n' )

    x2 = ''

    if ( outputNetList[ 0 ]._X2_WIDTH > 0 ): x2 = ', x2'

    code.write( 'def outputNet( x1{} ):\n'.format( x2 ) )
    code.write( '\n' )
    code.write( '    q = 0\n' )

    for net in outputNetList:

        code.write( '    {}\n'.format( net.generatePython() ) )

    code.write( '    return q\n' )

    code.write( '\n' )
    code.write( 'def transition( e, q1 ):\n'.format( x2 ) )
    code.write( '\n' )
    code.write( '    q = 0\n' )
    code.write( '\n' )

    c = 'if'

    for state in fsm.getStateList():


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
    code.write( '\n' )
    code.write( '    q_t = 0\n' )
    code.write( '\n' )
    code.write( '    for i in range( size ):\n' )
    code.write( '\n' )
    code.write( '        seed = getRandomInput( seed ) & 0xffffffff\n' )
    code.write( '\n' )
    code.write( '        x1   = seed\n' )
    code.write( '\n' )
    code.write( '        e    = inputNet( x1 )\n' )
    code.write( '\n' )
    code.write( '        q_t1 = transition( x1, q_t )\n' )
    code.write( '\n' )
    code.write( '        print "{}, {}->{}, {:08x}".format( q_t, q_t, q_t1, e )\n' )
    code.write( '\n' )
    code.write( '        q_t  = q_t1\n' )
    code.write( '\n' )
    code.write( 'size = {}\n'.format( ITERATIONS ) )
    code.write( 'seed = {}\n'.format( 42 ) )
    code.write( '\n' )
    code.write( 'print \'state, transition, input\'\n' )
    code.write( '\n' )
    code.write( 'controlLoop( size, seed )\n' )

def getSclOptimization( version ):
    s = '{ S7_Optimized_Access := '

    if ( version == SCL_S7_1500 ): s += '\'TRUE\''
    else: s += '\'FALSE\''

    s += ' }'

    return s

def generateScl( fsm, inputNetList, outputNetList, ITERATIONS, version, repeat ):

    code = open( 'fsm_{}.scl'.format( version ), 'w' )

    for count in range( repeat ):

        x2 = ''

        if ( inputNetList[ 0 ]._X2_WIDTH > 0 ): x2 = ', x2'

        code.write( 'function "inputNet{}" : void\n'.format( count ) )
        code.write( '{}\n'.format( getSclOptimization( version ) ) )
        code.write( 'version : 0.1\n' )
        code.write( '    var_input\n' )
        code.write( '        x1 : dword;\n' )
        code.write( '    end_var\n' )
        code.write( '    var_output\n' )
        code.write( '        y  : dword;\n' )
        code.write( '    end_var\n' )

        if ( version == SCL_S7_300 ):

            code.write( '    var_temp\n' )
            code.write( '        x_i  : dword;\n' )
            code.write( '        x1b_i at x_i : array[ 0 .. 31 ] of bool;\n' )
            code.write( '        y_i  : dword;\n' )
            code.write( '        yb_i at y_i : array[ 0 .. 31 ] of bool;\n' )
            code.write( '    end_var\n' )

        code.write( '\n' )
        code.write( 'begin\n' )
        code.write( '\n' )

        if ( version == SCL_S7_300 ):
            code.write( '    #x_i := #x;\n' )
            code.write( '\n' )

        for net in inputNetList:

            code.write( '    {}\n'.format( net.generateScl( version ) ) )
            code.write( '\n' )

        if ( version == SCL_S7_300 ):

            code.write( '    #y := #y_i;\n' )
            code.write( '\n' )

        code.write( 'end_function\n' )

        code.write( '\n' )
        code.write( 'function "transition{}" : void\n'.format( count ) )
        code.write( '{}\n'.format( getSclOptimization( version ) ) )
        code.write( 'version : 0.1\n' )
        code.write( '    var_input\n' )
        code.write( '        e  : dword;\n' )
        code.write( '        q  : dword;\n' )
        code.write( '    end_var\n' )
        code.write( '    var_output\n' )
        code.write( '        y  : dword;\n' )
        code.write( '    end_var\n' )
        code.write( '    var_temp\n' )
        code.write( '        q1 : dword;\n' )
        code.write( '        i  : dword;\n' )
        code.write( '    end_var\n' )
        code.write( '\n' )
        code.write( 'begin\n' )
        code.write( '\n' )
        code.write( '    #q1 := 0;\n' )
        code.write( '\n' )

        c = 'if'

        for state in fsm.getStateList():

            code.write( '    {} ( #q = {} ) then\n'.format( c, state.getNumber()) )

            state.generateScl( code )

            c = 'elsif'

        code.write( '    end_if;\n' )
        code.write( '\n' )

        code.write( '    #y := #q1;\n' )

        code.write( '\n' )
        code.write( 'end_function\n' )

        code.write( '\n' )
        code.write( 'function "getRandomInput" : void\n' )
        code.write( '{}\n'.format( getSclOptimization( version ) ) )
        code.write( 'version : 0.1\n' )
        code.write( '    var_input\n' )
        code.write( '        seed : dword;\n' )
        code.write( '    end_var\n' )
        code.write( '    var_output\n' )
        code.write( '        y    : dword;\n' )
        code.write( '    end_var\n' )
        code.write( '    var_temp\n' )
        code.write( '        r    : int;\n' )
        code.write( '        p1   : dint;\n' )
        code.write( '        p2   : dint;\n' )
        code.write( '        p3   : dint;\n' )
        code.write( '    end_var\n' )
        code.write( '\n' )
        code.write( 'begin\n' )
        code.write( '\n' )
        code.write( '    #r  := lfsr14( seed := dword_to_int( #seed ) );\n' )
        code.write( '    #p1 := dword_to_dint( SHL( IN := int_to_dword( #r ), N := 28 ) );\n' )
        code.write( '    #p2 := dword_to_dint( SHL( IN := int_to_dword( #r ), N := 14 ) );\n' )
        code.write( '    #p3 := int_to_dint( #r );\n' )
        code.write( '    #y  := dint_to_dword( p1 + p2 + p3 );\n' )

        code.write( '\n' )
        code.write( 'end_function\n' )

        code.write( '\n' )
        code.write( 'function "outputNet{}" : void\n'.format( count ) )
        code.write( '{}\n'.format( getSclOptimization( version ) ) )
        code.write( 'version : 0.1\n' )
        code.write( '    var_input\n' )
        code.write( '        x1 : dword;\n' )
        code.write( '        x2 : dword;\n' )
        code.write( '    end_var\n' )
        code.write( '    var_output\n' )
        code.write( '        y : dword;\n' )
        code.write( '    end_var\n' )
        code.write( '    var_temp\n' )
        code.write( '        x1_i         : dword;\n' )
        code.write( '        x1b_i at x_i : array[ 0 .. 31 ] of bool;\n' )
        code.write( '        x2_i         : dword;\n' )
        code.write( '        x2b_i at x_i : array[ 0 .. 31 ] of bool;\n' )
        code.write( '        y_i          : dword;\n' )
        code.write( '        yb_i at y_i  : array[ 0 .. 31 ] of bool;\n' )
        code.write( '    end_var\n' )
        code.write( '\n' )
        code.write( 'begin\n' )
        code.write( '\n' )
        code.write( '    #x1_i := #x1;\n' )
        code.write( '    #x2_i := #x2;\n' )
        code.write( '\n' )

        for net in outputNetList:

            code.write( '    {}\n'.format( net.generateScl( version ) ) )

        code.write( '\n' )
        code.write( '    #y := #y_i;\n' )
        code.write( '\n' )
        code.write( 'end_function\n' )

        code.write( '\n' )
        code.write( 'function "controlLoop{}" : void\n'.format( count ) )
        code.write( '{}\n'.format( getSclOptimization( version ) ) )
        code.write( 'version : 0.1\n' )
        code.write( '    var_input\n' )
        code.write( '        size  : dint;\n' )
        code.write( '        seedi : dword;\n' )
        code.write( '    end_var\n' )
        code.write( '    var_temp\n' )
        code.write( '        q    : dword;\n' )
        code.write( '        q1   : dword;\n' )
        code.write( '        x1   : dword;\n' )
        code.write( '        e    : dword;\n' )
        code.write( '        a    : dword;\n' )
        code.write( '        i    : dint;\n' )
        code.write( '        seed : dword;\n' )
        code.write( '    end_var\n' )
        code.write( '\n' )
        code.write( 'begin\n' )
        code.write( '\n' )
        code.write( '    #q    := 0;\n' )
        code.write( '    #seed := seedi;\n' )
        code.write( '\n' )
        code.write( '    for #i := 0 to #size - 1 do\n' )
        code.write( '\n' )
        code.write( '        "getRandomInput"( seed := #seed, y => #seed  );\n' )
        code.write( '\n' )
        code.write( '        #x1   := #seed;\n' )
        code.write( '\n' )
        code.write( '        "inputNet{}"( x := #x1, y => #e );\n'.format( count ) )
        code.write( '\n' )
        code.write( '        "transition{}"( e := #e, q := #q, y => #q1 );\n' .format( count ))
        code.write( '\n' )
        code.write( '        "states{}".q[ #i ] := #q;\n'.format( count ) )
        code.write( '\n' )
        code.write( '        #q := #q1;\n' )
        code.write( '\n' )
        code.write( '        "outputNet{}"( x1 := #q1, x2 := e, y => #a );\n'.format( count ) )
        code.write( '\n' )
        code.write( '    end_for;\n' )
        code.write( '\n' )
        code.write( 'end_function\n' )
        code.write( '\n' )
