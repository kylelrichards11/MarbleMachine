from components import IO, Replacer, Sorter, BlackBox
from machine import Connection, SharedLayer


##############################################################################################################################
class And(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'And'
    
        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        r2 = Replacer(['all'], ['blue'], name=f'{self.name} r2')
        input = IO(balls=['dark green'], name=f'{self.name} input')
        s1 = Sorter([('red', 'blue', 'dark green')], name=f'{self.name} s1')
        r3 = Replacer(['red', 'blue', 'dark green'], ['red'], name=f'{self.name} r3')

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(r3, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s1),
            Connection(input, s1),
            Connection(s1, r3)
        ]

##############################################################################################################################
class Binary4Bit(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'To 4-Bit\nBinary'

        sub1 = SubIfGreaterEqual(show_all=show_all)
        sub2 = SubIfGreaterEqual(show_all=show_all)
        sub3 = SubIfGreaterEqual(show_all=show_all)
        sub4 = SubIfGreaterEqual(show_all=show_all)
        io1 = IO(balls=['blue']*8)
        io2 = IO(balls=['blue']*4)
        io3 = IO(balls=['blue']*2)
        io4 = IO(balls=['blue'])

        self.inputs = [(sub1, 0)]
        self.outputs = [(sub1, 0), (sub2, 0), (sub3, 0), (sub4, 0)]

        self.connections = [
            Connection(io1, sub1, comp_to_input=1),
            Connection(sub1, sub2, comp_from_output=1),
            Connection(io2, sub2, comp_to_input=1),
            Connection(sub2, sub3, comp_from_output=1),
            Connection(io3, sub3, comp_to_input=1),
            Connection(sub3, sub4, comp_from_output=1),
            Connection(io4, sub4, comp_to_input=1)
        ]

##############################################################################################################################
class BinaryRelease4(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = '4-Bit\nRelease'

        rort1 = ReleaseOrThru(show_all=show_all)
        rort2 = ReleaseOrThru(show_all=show_all)
        rort3 = ReleaseOrThru(show_all=show_all)
        rort4 = ReleaseOrThru(show_all=show_all)

        self.inputs = [(rort4, 0), (rort3, 0), (rort2, 0), (rort1, 0), (rort1, 1)]
        self.outputs = [(rort4, 1), (rort4, 0), (rort3, 0), (rort2, 0), (rort1, 0)]

        self.connections = [
            Connection(rort1, rort2, comp_from_output=0, comp_to_input=1, reverse=True),
            Connection(rort2, rort3, comp_from_output=0, comp_to_input=1, reverse=True),
            Connection(rort3, rort4, comp_from_output=0, comp_to_input=1, reverse=True)
        ]

        self.shared_layers = [
            SharedLayer(rort1, rort2),
            SharedLayer(rort2, rort3),
            SharedLayer(rort3, rort4),
        ]

##############################################################################################################################
class Decrement(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Dec'
        
        input = IO(balls=['blue'], name=f'{self.name} input')
        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        s1 = Sorter([('red', 'blue'), ('red',)], name=f'{self.name} s1')

        self.inputs = [(r1, 0)]
        self.outputs = [(s1, 1)]

        self.connections = [
            Connection(r1, s1),
            Connection(input, s1)
        ]

##############################################################################################################################
class Equals(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Equals'

        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        r2 = Replacer(['all'], ['blue'], name=f'{self.name} r2')
        s1 = Sorter([('red', 'blue'), ('red',), ('blue',)], name=f'{self.name} s1')
        not_block = Not(show_all=show_all)

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(not_block, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s1),
            Connection(s1, not_block, comp_from_output=1),
            Connection(s1, not_block, comp_from_output=2)
        ]

        self.shared_layers = [
            SharedLayer(r1, r2)
        ]

##############################################################################################################################
class Eq2or3(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = '= 2 or 3'

        in2 = IO(balls=['blue']*2)
        in3 = IO(balls=['blue']*3)

        r1 = Replacer(['all'], ['red', 'blue'])
        s1 = Sorter([('red',), ('blue',)])
        eq2 = Equals(show_all=show_all)
        eq3 = Equals(show_all=show_all)
        or_block = Or(show_all=show_all)

        self.inputs = [(r1, 0)]
        self.outputs = [(or_block, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(in2, eq2),
            Connection(s1, eq2, comp_to_input=1),
            Connection(s1, eq3, comp_from_output=1),
            Connection(in3, eq3, comp_to_input=1),
            Connection(eq2, or_block),
            Connection(eq3, or_block, comp_to_input=1),
        ]

        self.shared_layers = [
            SharedLayer(in2, s1),
            SharedLayer(s1, in3)
        ]

##############################################################################################################################
class FSMIsOdd(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'FSM Is Odd'

        io1 = IO(balls=['red'])
        to_bin = Binary4Bit(show_all=show_all)
        br4 = BinaryRelease4(show_all=show_all)
        r0 = Replacer(['all'], ['dark green'])
        s1 = Sorter([('blue', 'purple'), ('red', 'dark green'), ('red',), ('blue', 'dark green'), ('blue',)])
        s2 = Sorter([('red',), ('blue',), ('purple',)])
        r1 = Replacer(['red', 'dark green'], ['blue', 'purple'])
        r2 = Replacer(['red'], ['red', 'purple'])
        r3 = Replacer(['blue', 'dark green'], ['blue', 'purple'])
        r4 = Replacer(['blue'], ['red', 'purple'])
        r5 = Replacer(['all'], ['purple'])

        self.inputs = [(to_bin, 0)]
        self.outputs = [(s1, 0)]

        self.connections = [
            Connection(to_bin, br4, comp_from_output=0, comp_to_input=0),
            Connection(to_bin, br4, comp_from_output=1, comp_to_input=1),
            Connection(to_bin, br4, comp_from_output=2, comp_to_input=2),
            Connection(to_bin, br4, comp_from_output=3, comp_to_input=3),
            Connection(io1, s1),
            Connection(br4, r5, comp_from_output=0),
            Connection(br4, r0, comp_from_output=1),
            Connection(br4, r0, comp_from_output=2),
            Connection(br4, r0, comp_from_output=3),
            Connection(br4, r0, comp_from_output=4),
            Connection(r0, s1),
            Connection(r5, s1),
            Connection(s1, r1, comp_from_output=1),
            Connection(s1, r2, comp_from_output=2),
            Connection(s1, r3, comp_from_output=3),
            Connection(s1, r4, comp_from_output=4),
            Connection(r1, s2),
            Connection(r2, s2),
            Connection(r3, s2),
            Connection(r4, s2),
            Connection(s2, s1, comp_from_output=0, reverse=True),
            Connection(s2, s1, comp_from_output=1, reverse=True),
            Connection(s2, br4, comp_from_output=2, comp_to_input=4, reverse=True),
        ]

        self.shared_layers = [
            SharedLayer(r0, io1)
        ]

##############################################################################################################################

class GreaterEqualThan(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = '>='

        r1 = Replacer(['all'], ['red', 'blue'])
        r2 = Replacer(['all'], ['red', 'blue'])
        s1 = Sorter([('red',), ('blue',)])
        s2 = Sorter([('red',), ('blue',)])
        greater = GreaterThan(show_all=show_all)
        equal = Equals(show_all=show_all)
        or_block = Or(show_all=show_all)

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(or_block, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s2),
            Connection(s1, greater, comp_from_output=0, comp_to_input=0),
            Connection(s1, equal, comp_from_output=1, comp_to_input=0),
            Connection(s2, greater, comp_from_output=0, comp_to_input=1),
            Connection(s2, equal, comp_from_output=1, comp_to_input=1),
            Connection(greater, or_block),
            Connection(equal, or_block, comp_to_input=1),
        ]

        self.shared_layers = [
            SharedLayer(r1, r2),
            SharedLayer(s1, s2)
        ]

##############################################################################################################################
class GreaterThan(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = '>'

        sub_block = Subtract(show_all=show_all)
        to_bool = ToBool(show_all=show_all)

        self.inputs = [(sub_block, 0), (sub_block, 1)]
        self.outputs = [(to_bool, 0)]

        self.connections = [
            Connection(sub_block, to_bool)
        ]

##############################################################################################################################
class Hold(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Hold'

        r1 = Replacer(['all'], ['red', 'blue'])
        s1 = Sorter([('red',), ('blue',)])
        mult = Multiply(show_all=False)
        r2 = Replacer(['all'], ['blue'])
        s2 = Sorter([('red', 'blue')])
        r3 = Replacer(['red', 'blue'], ['red'])

        self.inputs = [(r1, 0), (mult, 1)]
        self.outputs = [(r3, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(s1, mult, comp_from_output=1),
            Connection(mult, r2),
            Connection(r2, s2, reverse=True),
            Connection(s1, s2, comp_from_output=0),
            Connection(s2, r3)
        ]

##############################################################################################################################
class IfElse(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'If Else'

        r1 = Replacer(['all'], ['red'])
        io1 = IO(balls=['blue'])
        s1 = Sorter([('red', 'blue'), ('blue',)])

        self.inputs = [(r1, 0)]
        self.outputs = [(s1, 0), (s1, 1)]

        self.connections = [
            Connection(r1, s1),
            Connection(io1, s1)
        ]

##############################################################################################################################
class LessThan(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = '<'

        sub_block = Subtract(show_all=show_all)
        to_bool = ToBool(show_all=show_all)

        self.inputs = [(sub_block, 1), (sub_block, 0)]
        self.outputs = [(to_bool, 0)]

        self.connections = [
            Connection(sub_block, to_bool)
        ]


##############################################################################################################################
class Max(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Max'

        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        r2 = Replacer(['all'], ['blue'], name=f'{self.name} r2')
        r3 = Replacer(['red', 'blue'], ['red'], name=f'{self.name} r3')
        r4 = Replacer(['blue'], ['red'], name=f'{self.name} r4')
        s1 = Sorter([('red', 'blue'), ('red',), ('blue',)], name=f'{self.name} s1')
        s2 = Sorter([('red',)], name=f'{self.name} s2')

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(s2, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s1),
            Connection(s1, r3, comp_from_output=0),
            Connection(s1, r4, comp_from_output=2),
            Connection(r3, s2),
            Connection(r4, s2),
            Connection(s1, s2, comp_from_output=1)
        ]

##############################################################################################################################
class Min(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Min'

        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        r2 = Replacer(['all'], ['blue'], name=f'{self.name} r2')
        r3 = Replacer(['red', 'blue'], ['red'], name=f'{self.name} r3')
        s1 = Sorter([('red', 'blue'), ('red',), ('blue',)], name=f'{self.name} s1')

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(r3, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s1),
            Connection(s1, r3),
        ]

##############################################################################################################################
class Multiply(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        
        self.name = 'Multiply'

        sort2 = Sort_2(show_all=show_all)
        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        r2 = Replacer(['all'], ['blue'], name=f'{self.name} r2')
        s1 = Sorter([('red', 'blue'), ('blue',)], name=f'{self.name} s1')
        dec = Decrement(show_all=show_all)
        r3 = Replacer(['red', 'blue'], ['red', 'blue', 'dark green'], name=f'{self.name} r3')
        s2 = Sorter([('red',), ('blue',), ('dark green',)], name=f'{self.name} s2')

        self.inputs = [(sort2, 0), (sort2, 1)]
        self.outputs = [(s2, 2)]
        
        self.connections = [
            Connection(sort2, r1, comp_from_output=0),
            Connection(sort2, r2, comp_from_output=1),
            Connection(r1, s1),
            Connection(r2, s1),
            Connection(s1, r3, comp_from_output=0),
            Connection(s1, dec, comp_from_output=1),
            Connection(dec, sort2, comp_to_input=1, reverse=True),
            Connection(r3, s2),
            Connection(s2, sort2, comp_from_output=0, comp_to_input=0, reverse=True),
            Connection(s2, dec, comp_from_output=1)
        ]

##############################################################################################################################
class Not(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Not'

        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        input = IO(balls=['blue'], name=f'{self.name} input')
        s1 = Sorter([('red', 'blue'), ('blue',)], name=f'{self.name} s1')

        self.inputs = [(r1, 0)]
        self.outputs = [(s1, 1)]

        self.connections = [
            Connection(r1, s1),
            Connection(input, s1)
        ]

##############################################################################################################################
class Or(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Or'

        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        r2 = Replacer(['all'], ['red'], name=f'{self.name} r2')
        input = IO(balls=['blue'], name=f'{self.name} input')
        s1 = Sorter([('red', 'blue')], name=f'{self.name} s1')
        r3 = Replacer(['red', 'blue'], ['red'], name=f'{self.name} r3')

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(r3, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s1),
            Connection(input, s1),
            Connection(s1, r3)
        ]

##############################################################################################################################
class Plus1Div2(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = '+1,/2'

        r1 = Replacer(['all'], ['blue'])
        io1 = IO(balls=['blue'])
        s1 = Sorter([('blue', 'blue')])
        r2 = Replacer(['blue', 'blue'], ['blue'])

        self.inputs = [(r1, 0)]
        self.outputs = [(r2, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(io1, s1),
            Connection(s1, r2)
        ]


##############################################################################################################################
class ReleaseOrThru(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Release or Thru'

        tobool = ToBool(show_all=show_all)
        hold = Hold(show_all=show_all)
        r1 = Replacer(['all'], ['red', 'blue'])
        s1 = Sorter([('red', 'dark green'), ('blue',)])
        s2 = Sorter([('red', 'blue', 'blue')])
        s3 = Sorter([('red', 'blue'), ('blue',)])
        io1 = IO(balls=['dark green'])
        io2 = IO(balls=['red'])

        self.inputs = [(hold, 0), (tobool, 0)]
        self.outputs = [(hold, 0), (s3, 1)]

        self.connections = [
            Connection(tobool, r1),
            Connection(r1, s1),
            Connection(io1, s1),
            Connection(s1, hold, comp_to_input=1),
            Connection(s1, s2, comp_from_output=1),
            Connection(io2, s2),
            Connection(s2, s3),
            Connection(s3, s2, reverse=True)
        ]

##############################################################################################################################
class Sort_2(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Sort 2'

        r1 = Replacer(['all'], ['red', 'blue'])
        r2 = Replacer(['all'], ['red', 'blue'])
        s1 = Sorter([('red',), ('blue',)])
        s2 = Sorter([('red',), ('blue',)])
        min_block = Min(show_all=show_all)
        max_block = Max(show_all=show_all)

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(min_block, 0), (max_block, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s2),
            Connection(s1, min_block, comp_from_output=0, comp_to_input=0),
            Connection(s1, max_block, comp_from_output=1, comp_to_input=0),
            Connection(s2, min_block, comp_from_output=0, comp_to_input=1),
            Connection(s2, max_block, comp_from_output=1, comp_to_input=1),
        ]

        self.shared_layers = [
            SharedLayer(r1, r2),
            SharedLayer(s1, s2)
        ]

##############################################################################################################################
class SubIfGreater(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Sub If >'

        r1 = Replacer(['all'], ['red', 'blue'])
        r2 = Replacer(['all'], ['red', 'blue'])
        r3 = Replacer(['red'], ['red', 'blue'])
        r4 = Replacer(['all'], ['red', 'blue'])
        r5 = Replacer(['all'], ['red'])
        r6 = Replacer(['all'], ['red'])
        s1 = Sorter([('red',), ('blue',)])
        s2 = Sorter([('red',), ('blue',)])
        s3 = Sorter([('red',), ('blue',)])
        s4 = Sorter([('red',), ('blue',)])
        s5 = Sorter([('red',)])
        greater = GreaterThan(show_all=show_all)
        ifelse = IfElse(show_all=show_all)
        hold1 = Hold(show_all=show_all)
        hold2 = Hold(show_all=show_all)
        sub = Subtract(show_all=show_all)

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(s4, 1), (s5, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s2),
            Connection(s1, r3),
            Connection(s1, greater, comp_from_output=1, comp_to_input=0),
            Connection(s2, greater, comp_from_output=0, comp_to_input=1),
            Connection(r3, s3),
            Connection(s3, hold1),
            Connection(greater, ifelse),
            Connection(ifelse, hold1, comp_to_input=1),
            Connection(ifelse, r4, comp_from_output=1),
            Connection(r4, s4),
            Connection(s4, hold2, comp_to_input=1),
            Connection(s3, hold2, comp_from_output=1),
            Connection(hold2, sub),
            Connection(s2, sub, comp_from_output=1, comp_to_input=1),
            Connection(hold1, r5),
            Connection(sub, r6),
            Connection(r5, s5),
            Connection(r6, s5),
        ]

        self.shared_layers = [
            SharedLayer(r1, r2),
            SharedLayer(s1, s2)
        ]

##############################################################################################################################
class SubIfGreaterEqual(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Sub If >='

        r1 = Replacer(['all'], ['red', 'blue'])
        r2 = Replacer(['all'], ['red', 'blue'])
        r3 = Replacer(['red'], ['red', 'blue'])
        r4 = Replacer(['all'], ['red', 'blue'])
        r5 = Replacer(['all'], ['red'])
        r6 = Replacer(['all'], ['red'])
        s1 = Sorter([('red',), ('blue',)])
        s2 = Sorter([('red',), ('blue',)])
        s3 = Sorter([('red',), ('blue',)])
        s4 = Sorter([('red',), ('blue',)])
        s5 = Sorter([('red',)])
        greater = GreaterEqualThan(show_all=show_all)
        ifelse = IfElse(show_all=show_all)
        hold1 = Hold(show_all=show_all)
        hold2 = Hold(show_all=show_all)
        sub = Subtract(show_all=show_all)

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(s4, 1), (s5, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s2),
            Connection(s1, r3),
            Connection(s1, greater, comp_from_output=1, comp_to_input=0),
            Connection(s2, greater, comp_from_output=0, comp_to_input=1),
            Connection(r3, s3),
            Connection(s3, hold1),
            Connection(greater, ifelse),
            Connection(ifelse, hold1, comp_to_input=1),
            Connection(ifelse, r4, comp_from_output=1),
            Connection(r4, s4),
            Connection(s4, hold2, comp_to_input=1),
            Connection(s3, hold2, comp_from_output=1),
            Connection(hold2, sub),
            Connection(s2, sub, comp_from_output=1, comp_to_input=1),
            Connection(hold1, r5),
            Connection(sub, r6),
            Connection(r5, s5),
            Connection(r6, s5),
        ]

        self.shared_layers = [
            SharedLayer(r1, r2),
            SharedLayer(s1, s2)
        ]

##############################################################################################################################
class Subtract(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Sub'

        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        r2 = Replacer(['all'], ['blue'], name=f'{self.name} r2')
        s1 = Sorter([('red', 'blue'), ('red',), ('blue',)], name=f'{self.name} s1')

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(s1, 1)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s1, comp_to_input=1)
        ]

        self.shared_layers = [
            SharedLayer(r1, r2)
        ]

##############################################################################################################################
class ToBool(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'To Bool'

        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        io1 = IO(balls=['blue'], name=f'{self.name} io1')
        s1 = Sorter([('red', 'blue')], name=f'{self.name} s1')
        r2 = Replacer(['red', 'blue'], ['red'], name=f'{self.name} r2')

        self.inputs = [(r1, 0)]
        self.outputs = [(r2, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(io1, s1),
            Connection(s1, r2)
        ]


##############################################################################################################################
__all__ = {
    'And': And,
    'BinaryRelease4': BinaryRelease4,
    'Binary4Bit': Binary4Bit,
    'Decrement': Decrement,
    'Equals': Equals,
    'Eq2or3': Eq2or3,
    'FSMIsOdd': FSMIsOdd,
    'GreaterThan': GreaterThan,
    'GreaterEqualThan': GreaterEqualThan,
    'Hold': Hold,
    'IfElse': IfElse,
    'LessThan': LessThan,
    'Max': Max,
    'Min': Min,
    'Multiply': Multiply,
    'Not': Not,
    'Or': Or,
    'Plus1Div2': Plus1Div2,
    'ReleaseOrThru': ReleaseOrThru,
    'Sort_2': Sort_2,
    'SubIfGreater': SubIfGreater,
    'SubIfGreaterEqual': SubIfGreaterEqual,
    'Subtract': Subtract,
    'ToBool': ToBool
}