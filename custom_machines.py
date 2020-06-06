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

        sort2 = Sort_2(show_all=False)
        r1 = Replacer(['all'], ['red'], name=f'{self.name} r1')
        r2 = Replacer(['all'], ['blue'], name=f'{self.name} r2')
        s1 = Sorter([('red', 'blue'), ('blue',)], name=f'{self.name} s1')
        dec = Decrement(show_all=False)
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
class Sort_2(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Sort 2'

        r1 = Replacer(['all'], ['red', 'blue'], name=f'{self.name} r1')
        r2 = Replacer(['all'], ['red', 'blue'], name=f'{self.name} r2')
        s1 = Sorter([('red',), ('blue',)], name=f'{self.name} s1')
        s2 = Sorter([('red',), ('blue',)], name=f'{self.name} s2')
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
class Subtract(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Subtract'

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
    'Decrement': Decrement,
    'Equals': Equals,
    'GreaterThan': GreaterThan,
    'LessThan': LessThan,
    'Max': Max,
    'Min': Min,
    'Multiply': Multiply,
    'Not': Not,
    'Or': Or,
    'Sort_2': Sort_2,
    'Subtract': Subtract,
    'ToBool': ToBool
}