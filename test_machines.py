import argparse
import itertools

from tkinter import Tk

from components import IO
from machine import Machine, Connection, SharedLayer
import custom_machines

def test_machine(machine, show_all, fname=''):
    root = Tk()

    machine = machine(show_all=show_all)

    num_inputs = len(machine.inputs)
    num_outputs = len(machine.outputs)

    inputs = []
    outputs = []

    for i in range(num_inputs):
        inputs.append(IO(name=f'input_{i}'))

    for i in range(num_outputs):
        outputs.append(IO(name=f'output_{i}'))

    m = Machine(root)
    
    i = 0
    for input in inputs:
        m.add_connection(Connection(input, machine, comp_to_input=i))
        i += 1

    i = 0
    for output in outputs:
        m.add_connection(Connection(machine, output, comp_from_output=i))
        i += 1

    for comb in itertools.combinations(inputs, 2):
        m.add_shared_layer(SharedLayer(comb[0], comb[1]))

    for comb in itertools.combinations(outputs, 2):
        m.add_shared_layer(SharedLayer(comb[0], comb[1]))

    m.draw()
    if fname != '':
        m.save(fname)
    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--machine', type=str, help="Specific Machine to Test")
    parser.add_argument('--save', type=bool, help="Whether or not to save image")
    args = parser.parse_args()

    if args.machine is None:
        for machine in custom_machines.__all__:
            module_name = machine
            machine = custom_machines.__all__[machine]
            print(f"{module_name}: show_all={False}")
            test_machine(machine, False)
            print(f"{module_name}: show_all={True}")
            test_machine(machine, True)

    else:
        machine = custom_machines.__all__[args.machine]
        print(f"{args.machine}: show_all={False}")
        test_machine(machine, False)
        print(f"{args.machine}: show_all={True}")
        if args.save:
            test_machine(machine, True, args.machine)
        else:
            test_machine(machine, True)
        