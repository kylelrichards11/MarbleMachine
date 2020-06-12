from tkinter import *

from components import IO, Replacer, Sorter
from machine import Machine, Connection, SharedLayer
from custom_machines import Hold
        
if __name__ == "__main__":
    root = Tk()

    c1 = '#000000'
    c2 = '#333333'
    c3 = '#555555'
    c4 = '#888888'
    c5 = '#aaaaaa'
    c6 = '#cccccc'

    A = 'red'
    B = 'blue'
    halt = '#ff42a1'
    X = 'brown'
    Y = 'gold'
    left = 'dark green'
    right = 'purple'

    machine = Machine(root)

    temp = IO()

    tape1 = IO(balls=[c1])
    tape2 = IO(balls=[c2])
    tape3 = IO(balls=[c3])
    tape4 = IO(balls=[c4])
    tape5 = IO(balls=[c5])
    tape6 = IO(balls=[c6])

    hold1 = Hold(show_all=False)
    hold2 = Hold(show_all=False)
    hold3 = Hold(show_all=False)
    hold4 = Hold(show_all=False)
    hold5 = Hold(show_all=False)
    hold6 = Hold(show_all=False)

    init_state = IO(balls=['red'])

    sorter1 = Sorter([
        # Halt
        (halt,),
        # AX
        (A, X, c1),
        (A, X, c2),
        (A, X, c3),
        (A, X, c4),
        (A, X, c5),
        (A, X, c6),
        # AY
        (A, Y, c1),
        (A, Y, c2),
        (A, Y, c3),
        (A, Y, c4),
        (A, Y, c5),
        (A, Y, c6),
        # A (blank)
        (A, c1),
        (A, c2),
        (A, c3),
        (A, c4),
        (A, c5),
        (A, c6),
        # BX
        (B, X, c1),
        (B, X, c2),
        (B, X, c3),
        (B, X, c4),
        (B, X, c5),
        (B, X, c6),
        # BY
        (B, Y, c1),
        (B, Y, c2),
        (B, Y, c3),
        (B, Y, c4),
        (B, Y, c5),
        (B, Y, c6),
        # B (blank)
        (B, c1),
        (B, c2),
        (B, c3),
        (B, c4),
        (B, c5),
        (B, c6),
    ])
    # AX
    r1 = Replacer([A, X, c1], [B, Y, right, c1, c1])
    r2 = Replacer([A, X, c2], [B, Y, right, c2, c2])
    r3 = Replacer([A, X, c3], [B, Y, right, c3, c3])
    r4 = Replacer([A, X, c4], [B, Y, right, c4, c4])
    r5 = Replacer([A, X, c5], [B, Y, right, c5, c5])
    r6 = Replacer([A, X, c6], [B, Y, right, c6, c6])
    # AY
    r7 = Replacer([A, X, c1], [A, X, left, c1, c1])
    r8 = Replacer([A, X, c2], [A, X, left, c2, c2])
    r9 = Replacer([A, X, c3], [A, X, left, c3, c3])
    r10 = Replacer([A, X, c4], [A, X, left, c4, c4])
    r11 = Replacer([A, X, c5], [A, X, left, c5, c5])
    r12 = Replacer([A, X, c6], [A, X, left, c6, c6])
    # A (blank)
    r13 = Replacer([A, X, c1], [halt])
    r14 = Replacer([A, X, c2], [halt])
    r15 = Replacer([A, X, c3], [halt])
    r16 = Replacer([A, X, c4], [halt])
    r17 = Replacer([A, X, c5], [halt])
    r18 = Replacer([A, X, c6], [halt])
    # BX
    r19 = Replacer([B, X, c1], [B, X, right, c1, c1])
    r20 = Replacer([B, X, c2], [B, X, right, c2, c2])
    r21 = Replacer([B, X, c3], [B, X, right, c3, c3])
    r22 = Replacer([B, X, c4], [B, X, right, c4, c4])
    r23 = Replacer([B, X, c5], [B, X, right, c5, c5])
    r24 = Replacer([B, X, c6], [B, X, right, c6, c6])
    # BY
    r25 = Replacer([B, Y, c1], [B, Y, right, c1, c1])
    r26 = Replacer([B, Y, c2], [B, Y, right, c2, c2])
    r27 = Replacer([B, Y, c3], [B, Y, right, c3, c3])
    r28 = Replacer([B, Y, c4], [B, Y, right, c4, c4])
    r29 = Replacer([B, Y, c5], [B, Y, right, c5, c5])
    r30 = Replacer([B, Y, c6], [B, Y, right, c6, c6])
    # B (blank)
    r31 = Replacer([B, Y, c1], [A, Y, left, c1, c1])
    r32 = Replacer([B, Y, c2], [A, Y, left, c2, c2])
    r33 = Replacer([B, Y, c3], [A, Y, left, c3, c3])
    r34 = Replacer([B, Y, c4], [A, Y, left, c4, c4])
    r35 = Replacer([B, Y, c5], [A, Y, left, c5, c5])
    r36 = Replacer([B, Y, c6], [A, Y, left, c6, c6])


    sorter2 = Sorter([
        (A,),
        (B,),
        (halt,),
        (X, c1),
        (X, c2),
        (X, c3),
        (X, c4),
        (X, c5),
        (X, c6),
        (Y, c1),
        (Y, c2),
        (Y, c3),
        (Y, c4),
        (Y, c5),
        (Y, c6),
        (left, c1),
        (left, c2),
        (left, c3),
        (left, c4),
        (left, c5),
        (left, c6),
        (right, c1),
        (right, c2),
        (right, c3),
        (right, c4),
        (right, c5),
        (right, c6)
    ])

    machine.add_connection(Connection(tape1, hold1))
    machine.add_connection(Connection(tape2, hold2))
    machine.add_connection(Connection(tape3, hold3))
    machine.add_connection(Connection(tape4, hold4))
    machine.add_connection(Connection(tape5, hold5))
    machine.add_connection(Connection(tape6, hold6))

    machine.add_connection(Connection(init_state, sorter1))

    machine.add_connection(Connection(hold1, sorter1))
    machine.add_connection(Connection(hold2, sorter1))
    machine.add_connection(Connection(hold3, sorter1))
    machine.add_connection(Connection(hold4, sorter1))
    machine.add_connection(Connection(hold5, sorter1))
    machine.add_connection(Connection(hold6, sorter1))

    machine.add_connection(Connection(sorter1, r1, comp_from_output=1))
    machine.add_connection(Connection(sorter1, r2, comp_from_output=2))
    machine.add_connection(Connection(sorter1, r3, comp_from_output=3))
    machine.add_connection(Connection(sorter1, r4, comp_from_output=4))
    machine.add_connection(Connection(sorter1, r5, comp_from_output=5))
    machine.add_connection(Connection(sorter1, r6, comp_from_output=6))
    machine.add_connection(Connection(sorter1, r7, comp_from_output=7))
    machine.add_connection(Connection(sorter1, r8, comp_from_output=8))
    machine.add_connection(Connection(sorter1, r9, comp_from_output=9))
    machine.add_connection(Connection(sorter1, r10, comp_from_output=10))
    machine.add_connection(Connection(sorter1, r11, comp_from_output=11))
    machine.add_connection(Connection(sorter1, r12, comp_from_output=12))
    machine.add_connection(Connection(sorter1, r13, comp_from_output=13))
    machine.add_connection(Connection(sorter1, r14, comp_from_output=14))
    machine.add_connection(Connection(sorter1, r15, comp_from_output=15))
    machine.add_connection(Connection(sorter1, r16, comp_from_output=16))
    machine.add_connection(Connection(sorter1, r17, comp_from_output=17))
    machine.add_connection(Connection(sorter1, r18, comp_from_output=18))
    machine.add_connection(Connection(sorter1, r19, comp_from_output=19))
    machine.add_connection(Connection(sorter1, r20, comp_from_output=20))
    machine.add_connection(Connection(sorter1, r21, comp_from_output=21))
    machine.add_connection(Connection(sorter1, r22, comp_from_output=22))
    machine.add_connection(Connection(sorter1, r23, comp_from_output=23))
    machine.add_connection(Connection(sorter1, r24, comp_from_output=24))
    machine.add_connection(Connection(sorter1, r25, comp_from_output=25))
    machine.add_connection(Connection(sorter1, r26, comp_from_output=26))
    machine.add_connection(Connection(sorter1, r27, comp_from_output=27))
    machine.add_connection(Connection(sorter1, r28, comp_from_output=28))
    machine.add_connection(Connection(sorter1, r29, comp_from_output=29))
    machine.add_connection(Connection(sorter1, r30, comp_from_output=30))
    machine.add_connection(Connection(sorter1, r31, comp_from_output=31))
    machine.add_connection(Connection(sorter1, r32, comp_from_output=32))
    machine.add_connection(Connection(sorter1, r33, comp_from_output=33))
    machine.add_connection(Connection(sorter1, r34, comp_from_output=34))
    machine.add_connection(Connection(sorter1, r35, comp_from_output=35))
    machine.add_connection(Connection(sorter1, r36, comp_from_output=36))

    machine.add_connection(Connection(r1, sorter2))
    machine.add_connection(Connection(r2, sorter2))
    machine.add_connection(Connection(r3, sorter2))
    machine.add_connection(Connection(r4, sorter2))
    machine.add_connection(Connection(r5, sorter2))
    machine.add_connection(Connection(r6, sorter2))
    machine.add_connection(Connection(r7, sorter2))
    machine.add_connection(Connection(r8, sorter2))
    machine.add_connection(Connection(r9, sorter2))
    machine.add_connection(Connection(r10, sorter2))
    machine.add_connection(Connection(r11, sorter2))
    machine.add_connection(Connection(r12, sorter2))
    machine.add_connection(Connection(r13, sorter2))
    machine.add_connection(Connection(r14, sorter2))
    machine.add_connection(Connection(r15, sorter2))
    machine.add_connection(Connection(r16, sorter2))
    machine.add_connection(Connection(r17, sorter2))
    machine.add_connection(Connection(r18, sorter2))
    machine.add_connection(Connection(r19, sorter2))
    machine.add_connection(Connection(r20, sorter2))
    machine.add_connection(Connection(r21, sorter2))
    machine.add_connection(Connection(r22, sorter2))
    machine.add_connection(Connection(r23, sorter2))
    machine.add_connection(Connection(r24, sorter2))
    machine.add_connection(Connection(r25, sorter2))
    machine.add_connection(Connection(r26, sorter2))
    machine.add_connection(Connection(r27, sorter2))
    machine.add_connection(Connection(r28, sorter2))
    machine.add_connection(Connection(r29, sorter2))
    machine.add_connection(Connection(r30, sorter2))
    machine.add_connection(Connection(r31, sorter2))
    machine.add_connection(Connection(r32, sorter2))
    machine.add_connection(Connection(r33, sorter2))
    machine.add_connection(Connection(r34, sorter2))
    machine.add_connection(Connection(r35, sorter2))
    machine.add_connection(Connection(r36, sorter2))

    machine.add_connection(Connection(sorter2, sorter1, comp_from_output=0, reverse=True))
    machine.add_connection(Connection(sorter2, sorter1, comp_from_output=1, reverse=True))
    machine.add_connection(Connection(sorter2, sorter1, comp_from_output=2, reverse=True))

    machine.add_connection(Connection(sorter2, tape1, comp_from_output=3, reverse=True))
    machine.add_connection(Connection(sorter2, tape2, comp_from_output=4, reverse=True))
    machine.add_connection(Connection(sorter2, tape3, comp_from_output=5, reverse=True))
    machine.add_connection(Connection(sorter2, tape4, comp_from_output=6, reverse=True))
    machine.add_connection(Connection(sorter2, tape5, comp_from_output=7, reverse=True))
    machine.add_connection(Connection(sorter2, tape6, comp_from_output=8, reverse=True))
    machine.add_connection(Connection(sorter2, tape1, comp_from_output=9, reverse=True))
    machine.add_connection(Connection(sorter2, tape2, comp_from_output=10, reverse=True))
    machine.add_connection(Connection(sorter2, tape3, comp_from_output=11, reverse=True))
    machine.add_connection(Connection(sorter2, tape4, comp_from_output=12, reverse=True))
    machine.add_connection(Connection(sorter2, tape5, comp_from_output=13, reverse=True))
    machine.add_connection(Connection(sorter2, tape6, comp_from_output=14, reverse=True))

    machine.add_connection(Connection(sorter2, hold1, comp_from_output=16, comp_to_input=1, reverse=True))
    machine.add_connection(Connection(sorter2, hold2, comp_from_output=17, comp_to_input=1, reverse=True))
    machine.add_connection(Connection(sorter2, hold3, comp_from_output=18, comp_to_input=1, reverse=True))
    machine.add_connection(Connection(sorter2, hold4, comp_from_output=19, comp_to_input=1, reverse=True))
    machine.add_connection(Connection(sorter2, hold5, comp_from_output=20, comp_to_input=1, reverse=True))
    machine.add_connection(Connection(sorter2, hold2, comp_from_output=21, comp_to_input=1, reverse=True))
    machine.add_connection(Connection(sorter2, hold3, comp_from_output=22, comp_to_input=1, reverse=True))
    machine.add_connection(Connection(sorter2, hold4, comp_from_output=23, comp_to_input=1, reverse=True))
    machine.add_connection(Connection(sorter2, hold5, comp_from_output=24, comp_to_input=1, reverse=True))
    machine.add_connection(Connection(sorter2, hold6, comp_from_output=25, comp_to_input=1, reverse=True))

    machine.add_shared_layer(SharedLayer(hold6, init_state))

    machine.draw()
    mainloop()

# A:A# B:B# X:X# Y: Yellow
# Left: Green
# Right:right