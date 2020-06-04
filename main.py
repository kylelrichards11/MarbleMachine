from tkinter import Tk

from components import Sorter, Replacer, IO, BlackBox
from connector import Connector, Connection, SharedLayer
from modules import *
        
if __name__ == "__main__":
    root = Tk()
    show_all = True
    input1 = IO()
    input2 = IO()
    test_block = Decrement(show_all=show_all)
    output1 = IO()
    output2 = IO()

    input_layer = SharedLayer(input1, input2)
    output_layer = SharedLayer(output1, output2)

    con = Connector(root)
    con.connect(Connection(input1, test_block, el_to_input=0))
    # con.connect(Connection(input2, test_block, el_to_input=1))
    con.connect(Connection(test_block, output1, el_from_output=0))
    # con.connect(Connection(test_block, output2, el_from_output=1))

    con.add_shared_layer(input_layer)
    con.add_shared_layer(output_layer)

    con.draw()

    root.mainloop()