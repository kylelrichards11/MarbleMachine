import argparse
import itertools

from tkinter import Tk

from components import IO
from connector import Connector, Connection, SharedLayer
import modules

def test_module(module, show_all):
    root = Tk()

    module = module(show_all=show_all)

    num_inputs = len(module.inputs)
    num_outputs = len(module.outputs)

    inputs = []
    outputs = []

    for i in range(num_inputs):
        inputs.append(IO())

    for i in range(num_outputs):
        outputs.append(IO())

    con = Connector(root)
    
    i = 0
    for input in inputs:
        con.connect(Connection(input, module, el_to_input=i))
        i += 1

    i = 0
    for output in outputs:
        con.connect(Connection(module, output, el_from_output=i))
        i += 1

    for comb in itertools.combinations(inputs, 2):
        con.add_shared_layer(SharedLayer(comb[0], comb[1]))

    for comb in itertools.combinations(outputs, 2):
        con.add_shared_layer(SharedLayer(comb[0], comb[1]))

    con.draw()
    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', type=str, help="Specific Module to Test")
    args = parser.parse_args()

    if args.module is None:
        for module in modules.__all__:
            module_name = module
            module = modules.__all__[module]
            print(f"{module_name}: show_all={False}")
            test_module(module, False)
            print(f"{module_name}: show_all={True}")
            test_module(module, True)

    else:
        module = modules.__all__[args.module]
        # print(f"{args.module}: show_all={False}")
        # test_module(module, False)
        print(f"{args.module}: show_all={True}")
        test_module(module, True)
        