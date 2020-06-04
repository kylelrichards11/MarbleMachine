from components import IO, Replacer, Sorter, BlackBox
from connector import Connection, SharedLayer


##############################################################################################################################
class And(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'And'
    
        replacer1 = Replacer(['all'], ['red'])
        replacer2 = Replacer(['all'], ['blue'])
        input = IO(balls=['dark green'])
        sorter = Sorter([('red', 'blue', 'dark green')])
        replacer3 = Replacer(['red', 'blue', 'dark green'], ['red'])

        self.inputs = [(replacer1, 0), (replacer2, 0)]
        self.outputs = [(replacer3, 0)]

        self.connections = [
            Connection(replacer1, sorter),
            Connection(replacer2, sorter),
            Connection(input, sorter),
            Connection(sorter, replacer3)
        ]

##############################################################################################################################
class Decrement(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Decrement'
        
        input = IO(balls=['blue'])
        replacer = Replacer(['all'], ['red'])
        sorter = Sorter([('red', 'blue'), ('red',)])

        self.inputs = [(replacer, 0)]
        self.outputs = [(sorter, 1)]

        self.connections = [
            ((replacer, 0), (sorter, 0)),
            ((input, 0), (sorter, 0))
        ]

        self.connections = [
            Connection(replacer, sorter),
            Connection(input, sorter)
        ]

##############################################################################################################################
class Equals(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Equals'

        r1 = Replacer(['all'], ['red'])
        r2 = Replacer(['all'], ['blue'])
        s1 = Sorter([('red', 'blue'), ('red',), ('blue',)])
        not_block = Not(show_all=show_all)

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(not_block, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s1),
            Connection(s1, not_block, el_from_output=1),
            Connection(s1, not_block, el_from_output=2)
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

        r1 = Replacer(['all'], ['red'])
        r2 = Replacer(['all'], ['blue'])
        r3 = Replacer(['red', 'blue'], ['red'])
        r4 = Replacer(['blue'], ['red'])
        s1 = Sorter([('red', 'blue'), ('red',), ('blue',)])
        s2 = Sorter([('red',)])

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(s2, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s1),
            Connection(s1, r3, el_from_output=0),
            Connection(s1, r4, el_from_output=2),
            Connection(r3, s2),
            Connection(r4, s2),
            Connection(s1, s2, el_from_output=1)
        ]

##############################################################################################################################
class Min(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Min'

        r1 = Replacer(['all'], ['red'])
        r2 = Replacer(['all'], ['blue'])
        r3 = Replacer(['red', 'blue'], ['red'])
        s1 = Sorter([('red', 'blue'), ('red',), ('blue',)])

        self.inputs = [(r1, 0), (r2, 0)]
        self.outputs = [(r3, 0)]

        self.connections = [
            Connection(r1, s1),
            Connection(r2, s1),
            Connection(s1, r3),
        ]

##############################################################################################################################
class Not(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Not'

        replacer = Replacer(['all'], ['red'])
        input = IO(balls=['blue'])
        sorter = Sorter([('red', 'blue'), ('blue',)])

        self.inputs = [(replacer, 0)]
        self.outputs = [(sorter, 1)]

        self.connections = [
            Connection(replacer, sorter),
            Connection(input, sorter)
        ]

##############################################################################################################################
class Or(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'Or'

        replacer1 = Replacer(['all'], ['red'])
        replacer2 = Replacer(['all'], ['red'])
        input = IO(balls=['blue'])
        sorter = Sorter([('red', 'blue')])
        replacer3 = Replacer(['red', 'blue'], ['red'])

        self.inputs = [(replacer1, 0), (replacer2, 0)]
        self.outputs = [(replacer3, 0)]

        self.connections = [
            Connection(replacer1, sorter),
            Connection(replacer2, sorter),
            Connection(input, sorter),
            Connection(sorter, replacer3)
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
            Connection(s1, min_block, el_from_output=0, el_to_input=0),
            Connection(s1, max_block, el_from_output=1, el_to_input=0),
            Connection(s2, min_block, el_from_output=0, el_to_input=1),
            Connection(s2, max_block, el_from_output=1, el_to_input=1),
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

        replacer1 = Replacer(['all'], ['red'])
        replacer2 = Replacer(['all'], ['blue'])
        sorter = Sorter([('red', 'blue'), ('red',), ('blue',)])

        self.inputs = [(replacer1, 0), (replacer2, 0)]
        self.outputs = [(sorter, 1)]

        self.connections = [
            Connection(replacer1, sorter),
            Connection(replacer2, sorter, el_to_input=1)
        ]

        self.shared_layers = [
            SharedLayer(replacer1, replacer2)
        ]

##############################################################################################################################
class ToBool(BlackBox):
    def __init__(self, show_all=False):
        super().__init__(show_all=show_all)
        self.name = 'To Bool'

        r1 = Replacer(['all'], ['red'])
        io1 = IO(balls=['blue'])
        s1 = Sorter([('red', 'blue')])
        r2 = Replacer(['red', 'blue'], ['red'])

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
    
