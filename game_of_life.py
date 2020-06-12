from tkinter import *

from components import IO, Replacer, Sorter
from machine import Machine, Connection, SharedLayer
from custom_machines import Eq2or3
        
if __name__ == "__main__":
    root = Tk()
    machine = Machine(root)

    cell1 = IO()
    cell2 = IO()
    cell3 = IO()
    cell4 = IO()
    cell5 = IO()
    cell6 = IO()
    cell7 = IO()
    cell8 = IO()
    cell9 = IO()

    r_colors = ['red', 'blue', 'purple', 'dark green', 'gold', 'grey', 'orange', 'cyan']

    r1 = Replacer(['black'], r_colors)
    r2 = Replacer(['black'], r_colors)
    r3 = Replacer(['black'], r_colors)
    r4 = Replacer(['black'], r_colors)
    r5 = Replacer(['black'], r_colors)
    r6 = Replacer(['black'], r_colors)
    r7 = Replacer(['black'], r_colors)
    r8 = Replacer(['black'], r_colors)
    r9 = Replacer(['black'], r_colors)

    s1 = Sorter([('red',), ('blue',), ('purple',), ('dark green',), ('gold',), ('grey',), ('orange',), ('cyan',)])
    s2 = Sorter([('red',), ('blue',), ('purple',), ('dark green',), ('gold',), ('grey',), ('orange',), ('cyan',)])
    s3 = Sorter([('red',), ('blue',), ('purple',), ('dark green',), ('gold',), ('grey',), ('orange',), ('cyan',)])
    s4 = Sorter([('red',), ('blue',), ('purple',), ('dark green',), ('gold',), ('grey',), ('orange',), ('cyan',)])
    s5 = Sorter([('red',), ('blue',), ('purple',), ('dark green',), ('gold',), ('grey',), ('orange',), ('cyan',)])
    s6 = Sorter([('red',), ('blue',), ('purple',), ('dark green',), ('gold',), ('grey',), ('orange',), ('cyan',)])
    s7 = Sorter([('red',), ('blue',), ('purple',), ('dark green',), ('gold',), ('grey',), ('orange',), ('cyan',)])
    s8 = Sorter([('red',), ('blue',), ('purple',), ('dark green',), ('gold',), ('grey',), ('orange',), ('cyan',)])

    eq1 = Eq2or3(False)

    output = IO()

    machine.add_connection(Connection(cell1, r1))
    machine.add_connection(Connection(cell2, r2))
    machine.add_connection(Connection(cell3, r3))
    machine.add_connection(Connection(cell4, r4))
    machine.add_connection(Connection(cell6, r5))
    machine.add_connection(Connection(cell7, r6))
    machine.add_connection(Connection(cell8, r7))
    machine.add_connection(Connection(cell9, r8))

    machine.add_connection(Connection(r1, s1))
    machine.add_connection(Connection(r2, s2))
    machine.add_connection(Connection(r3, s3))
    machine.add_connection(Connection(r4, s4))
    machine.add_connection(Connection(r5, s5))
    machine.add_connection(Connection(r6, s6))
    machine.add_connection(Connection(r7, s7))
    machine.add_connection(Connection(r8, s8))

    machine.add_connection(Connection(s1, eq1, comp_from_output=0))
    machine.add_connection(Connection(s2, eq1, comp_from_output=1))
    machine.add_connection(Connection(s3, eq1, comp_from_output=2))
    machine.add_connection(Connection(s4, eq1, comp_from_output=3))
    machine.add_connection(Connection(s5, eq1, comp_from_output=4))
    machine.add_connection(Connection(s6, eq1, comp_from_output=5))
    machine.add_connection(Connection(s7, eq1, comp_from_output=6))
    machine.add_connection(Connection(s8, eq1, comp_from_output=7))

    machine.add_connection(Connection(eq1, output))

    machine.draw()
    mainloop()
