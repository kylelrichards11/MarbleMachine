from statistics import mean

from tkinter import *
from PIL import Image
import io

from components import BlackBox
from globals import GRID_SIZE

class Connection:
    """ Defines an ordered connection between two components

    Parameters
    ----------
    comp_from (Component): The component the marble comes from

    comp_to (Component): The component the marble goes to

    comp_from_output (int) default=0: The output number from the comp_from component

    comp_to_input (int) defualt=0: The input number to the comp_to component

    reverse (bool) default=False: Whether or not the connection goes from a lower component to a higher component

    Returns
    -------
    Connection: Initialized Connection object

    """
    def __init__(self, comp_from, comp_to, comp_from_output=0, comp_to_input=0, reverse=False):
        self.comp_from = comp_from
        self.comp_to = comp_to
        self.comp_from_output = comp_from_output
        self.comp_to_input = comp_to_input
        self.reverse = reverse

    def __str__(self):
        return f"From: {self.comp_from}, To: {self.comp_to}, From Output: {self.comp_from_output}, To Input: {self.comp_to_input}, Reverse: {self.reverse}"


class SharedLayer:
    """ Defines the order of two components that must be in the same layer

    Parameters
    ----------
    comp_left (Component): The component that must be on the left

    comp_right (Component): The component that must be on the right

    Returns
    -------
    SharedLayer: Initialized SharedLayer object

    """
    def __init__(self, comp_left, comp_right):
        self.comp_left = comp_left
        self.comp_right = comp_right

class Pair:
    """ A struct to hold Connection info with uuids

    Parameters
    ----------
    comp_from_uuid (int): The uuid of the from component

    comp_to_uuid (int): The uuid of the to component

    comp_from_output (int) default=0: The output number from the comp_from component

    comp_to_input (int) defualt=0: The input number to the comp_to component

    reverse (bool) default=False: Whether or not the connection goes from a lower component to a higher component

    Returns
    -------
    Pair: Initialized Pair object

    """
    def __init__(self, comp_from_uuid, comp_to_uuid, comp_from_output, comp_to_input, reverse):
        self.comp_from_uuid = comp_from_uuid
        self.comp_to_uuid = comp_to_uuid
        self.comp_from_output = comp_from_output
        self.comp_to_input = comp_to_input
        self.reverse = reverse

    def __str__(self):
        return f"From: {self.comp_from_uuid}, To: {self.comp_to_uuid}, From Output: {self.comp_from_output}, To Input: {self.comp_to_input}, Reverse: {self.reverse}"

    def __eq__(self, other):
        return (
            self.comp_from_uuid == other.comp_from_uuid 
            and self.comp_to_uuid == other.comp_to_uuid 
            and self.comp_from_output == other.comp_from_output
            and self.comp_to_input == other.comp_to_input
            and self.reverse == other.reverse
        )

class Machine:
    """ Defines a machine as a set of ordered connections and layers between components.

    Parameters
    ----------
    root: (tkinter.Tk.root()) default=None: The root Tk object. If None, then one is created.

    """
    def __init__(self, root=None):
        self.black_boxes_added = []
        self.canvas = None
        self.comp_layers = {}
        self.components = {}
        self.layers = {}
        self.pairs = []
        self.root = root
        self.shared_layer_orders = {}
        self.shared_layers = {}
        self.uuid_counter = 0

    # Private Methods
    def _add_black_box(self, comp):
        if comp.get_uuid() not in self.black_boxes_added:
            self._create_uuid(comp)
            self.black_boxes_added.append(comp.get_uuid())
            self.components[comp.get_uuid()] = comp
            for connection in comp.get_connections():
                self._add_component(connection.comp_from)
                self._add_component(connection.comp_to)
            for shared_layer in comp.get_shared_layers():
                self.add_shared_layer(shared_layer)

    def _add_component(self, comp):
        if isinstance(comp, BlackBox):
            self._add_black_box(comp)
        elif comp.get_uuid() == -1:
            self._create_uuid(comp)
            self.components[comp.get_uuid()] = comp

    def _add_to_layers(self, uuid, layer):
        if layer in self.layers:
            self.layers[layer].append(uuid)
        else:
            self.layers[layer] = [uuid]
        self.comp_layers[uuid] = layer

    def _calc_total_size(self):
        widths = self._get_layer_widths()
        heights = self._get_layer_heights()
        
        max_width = 0
        for layer in widths:
            max_width = max(max_width, widths[layer])

        total_height = 0
        for layer in heights:
            total_height += heights[layer]
            if heights[layer] > 0:
                total_height += 2*GRID_SIZE
        total_height -= 2*GRID_SIZE
        return max_width, total_height

    def _change_layer(self, uuid, new_layer, old_layer):
        if new_layer != old_layer:
            self.layers[old_layer].remove(uuid)
            self._add_to_layers(uuid, new_layer)
            # Change shared layer components
            if uuid in self.shared_layers:
                for shared_el in self.shared_layers[uuid]:
                    if shared_el in self.comp_layers:
                        self._change_layer(shared_el, new_layer, self.comp_layers[shared_el])
            # Change future components
            for pair in self.pairs:
                if pair.comp_from_uuid == uuid and not pair.reverse:
                    if pair.comp_to_uuid in self.comp_layers:
                        self._change_layer(pair.comp_to_uuid, new_layer+1, self.comp_layers[pair.comp_to_uuid])

    def _connect_black_box(self, comp_from, comp_to, comp_from_output, comp_to_input, reverse):
        self._add_component(comp_from)
        self._add_component(comp_to)
        
        if isinstance(comp_from, BlackBox) and isinstance(comp_to, BlackBox):
            for connection in comp_from.get_connections():
                self.add_connection(connection)
            self.add_connection(Connection(
                comp_from.outputs[comp_from_output][0], 
                comp_to.inputs[comp_to_input][0], 
                comp_to_input=comp_to.inputs[comp_to_input][1], 
                comp_from_output=comp_from.outputs[comp_from_output][1],
                reverse=reverse
            ))
            for connection in comp_to.get_connections():
                self.add_connection(connection)
        elif isinstance(comp_from, BlackBox):
            for connection in comp_from.get_connections():
                self.add_connection(connection)
            self.add_connection(Connection(
                comp_from.outputs[comp_from_output][0], 
                comp_to, 
                comp_to_input=comp_to_input, 
                comp_from_output=comp_from.outputs[comp_from_output][1],
                reverse=reverse
            ))
        else:
            self.add_connection(Connection(
                comp_from, 
                comp_to.inputs[comp_to_input][0], 
                comp_to_input=comp_to.inputs[comp_to_input][1], 
                comp_from_output=comp_from_output,
                reverse=reverse
            ))
            for connection in comp_to.get_connections():
                self.add_connection(connection)

    def _connect_component(self, comp_from, comp_to, comp_from_output, comp_to_input, reverse):
        self._add_component(comp_from)
        self._add_component(comp_to)

        from_uuid = comp_from.get_uuid()
        to_uuid = comp_to.get_uuid()

        pair = Pair(from_uuid, to_uuid, comp_from_output, comp_to_input, reverse)
        if pair not in self.pairs:
            self.pairs.append(pair)

    def _create_canvas(self, width, height):
        frame = Frame(self.root, width=width, height=height)
        frame.pack(expand=True, fill=BOTH)
        canvas = Canvas(frame, bg='#FFFFFF', width=width, height=height, scrollregion=(0, 0, width + 200, height + 200))
        hbar = Scrollbar(frame, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=canvas.xview)
        vbar = Scrollbar(frame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=width, height=height)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.pack(side=LEFT, expand=True, fill=BOTH)
        return canvas

    def _create_layers(self):
        for pair in self.pairs:
            from_uuid = pair.comp_from_uuid
            to_uuid = pair.comp_to_uuid
            if from_uuid in self.comp_layers and to_uuid in self.comp_layers:
                if self.comp_layers[to_uuid] <= self.comp_layers[from_uuid]:
                    if not pair.reverse:
                        self._change_layer(to_uuid, self.comp_layers[from_uuid] + 1, self.comp_layers[to_uuid])
            elif from_uuid in self.comp_layers:
                new_layer = self.comp_layers[from_uuid] + 1
                if to_uuid in self.shared_layers:
                    new_layer = self._get_shared_layer(to_uuid, new_layer)
                self._add_to_layers(to_uuid, new_layer)
            elif to_uuid in self.comp_layers:
                new_layer = self.comp_layers[to_uuid] - 1
                if from_uuid in self.shared_layers:
                    new_layer = self._get_shared_layer(from_uuid, new_layer)
                self._add_to_layers(from_uuid, new_layer)
            else:
                new_layer_from = 0
                if from_uuid in self.shared_layers:
                    new_layer_from = self._get_shared_layer(from_uuid, new_layer_from)
                self._add_to_layers(from_uuid, new_layer_from)

                new_layer_to = 1
                if to_uuid in self.shared_layers:
                    new_layer_to = self._get_shared_layer(to_uuid, new_layer_to)
                self._add_to_layers(to_uuid, new_layer_to)

    def _create_uuid(self, comp):
        assert(comp.get_uuid() == -1)
        comp.assign_uuid(self.uuid_counter)
        self.uuid_counter += 1

    def _generate_layer_order(self, orig_layer_uuids):
        order = []
        while(len(orig_layer_uuids) > 0):
            layer_uuids = []
            for uuid in orig_layer_uuids:
                if uuid in self.shared_layer_orders:
                    add_uuid = True
                    for shared_uuid in self.shared_layer_orders[uuid]:
                        if shared_uuid not in order:
                            add_uuid = False
                            break
                    if add_uuid:
                        order.append(uuid)
                    else:
                        layer_uuids.append(uuid)
                else:
                    order.append(uuid)
            orig_layer_uuids = layer_uuids
        return order

    def _get_canvas_dims(self):
        total_width, total_height = self._calc_total_size()
        canv_width = total_width + 2*GRID_SIZE
        canv_height = total_height + 2*GRID_SIZE
        return canv_height, canv_width

    def _get_layer_heights(self):
        heights = {}
        for layer in self.layers:
            height = 0
            for uuid in self.layers[layer]:
                comp = self.components[uuid]
                height = max(height, comp.get_height())
            heights[layer] = height
        return heights

    def _get_layer_widths(self):
        widths = {}
        for layer in self.layers:
            width = 0
            for uuid in self.layers[layer]:
                comp = self.components[uuid]
                width += comp.get_width()
                width += 2*GRID_SIZE
            width -= 2*GRID_SIZE
            widths[layer] = width
        return widths

    def _get_shared_layer(self, uuid, new_layer):
        shared_layer = new_layer
        for shared_el in self.shared_layers[uuid]:
            if shared_el in self.comp_layers:
                if new_layer > self.comp_layers[shared_el]:
                    self._change_layer(shared_el, new_layer, self.comp_layers[shared_el])
                shared_layer = self.comp_layers[shared_el]
        return shared_layer

    # Public Methods
    def add_connection(self, connection):
        """ Adds a connection to the Machine 
        
        Parameters
        ----------
        connection (Connection): The connection object to add

        Returns
        -------
        None
        
        """
        if (isinstance(connection.comp_from, BlackBox) and connection.comp_from.show_all) or (isinstance(connection.comp_to, BlackBox) and connection.comp_to.show_all):
            self._connect_black_box(connection.comp_from, connection.comp_to, connection.comp_from_output, connection.comp_to_input, connection.reverse)
        else:
            self._connect_component(connection.comp_from, connection.comp_to, connection.comp_from_output, connection.comp_to_input, connection.reverse)

    def add_shared_layer(self, layer):
        """ Adds a SharedLayer object to the connections 

        Parameters
        ----------
        layer (SharedLayer): The layer to add

        Returns
        -------
        None
        
        """
        comp_left_uuid = layer.comp_left.get_uuid()
        comp_right_uuid = layer.comp_right.get_uuid()
        if comp_left_uuid in self.shared_layers:
            self.shared_layers[comp_left_uuid].append(comp_right_uuid)
        else:
            self.shared_layers[comp_left_uuid] = [comp_right_uuid]
        if comp_right_uuid in self.shared_layers:
            self.shared_layers[comp_right_uuid].append(comp_left_uuid)
        else:
            self.shared_layers[comp_right_uuid] = [comp_left_uuid]
        if comp_right_uuid in self.shared_layer_orders:
            self.shared_layer_orders[comp_right_uuid].append(comp_left_uuid)
        else:
            self.shared_layer_orders[comp_right_uuid] = [comp_left_uuid]



    def draw(self, canvas=None, x=-1, y=-1):
        """ Draws the machine by assigning x and y coordinates to each component and drawing connections

        Parameters
        ----------
        canvas (tkinter.Canvas) default=None: The canvas to draw on. If none, a new canvas is made.

        x (int) default=-1: The x coordinate to center the machine on horizontally. If -1, the center of the canvas is used.

        y (int) default=-1: The y coordinate to center the machine on vertically. If -1, the center of the canvas is used.

        Returns
        -------
        None
        """

        # Assign Layers
        self._create_layers()

        # Define Canvas
        if canvas is None:
            canv_width, canv_height = self._get_canvas_dims()
            canv_width = max(1000, canv_width)
            canv_height = max(5000, canv_height)
            assert(self.root is not None)
            canvas = self._create_canvas(canv_width, canv_height)
            middle_x = canv_width/2
            start_y = 2*GRID_SIZE
        else:
            assert(x > 0)
            assert(y > 0)
            _, total_height = self._calc_total_size()
            middle_x = x
            start_y = y - total_height/2 - 2*GRID_SIZE

        # Draw Layers
        layer_widths = self._get_layer_widths()
        layer_heights = self._get_layer_heights()
        for layer in sorted(self.layers.keys()):
            start_x = middle_x - layer_widths[layer]/2
            y = start_y + layer_heights[layer]/2
            if len(self.layers[layer]) == 1 and layer != sorted(self.layers.keys())[0]:
                uuid = self.layers[layer][0]
                comp = self.components[uuid]
                prev_output_xs = []
                for pair in self.pairs:
                    if pair.comp_to_uuid == uuid and not pair.reverse:
                        prev_output_xs.append(self.components[pair.comp_from_uuid].get_output_coords(pair.comp_from_output)[0])
                avg_x = mean(prev_output_xs)
                comp.draw(canvas, avg_x, y)
            else:
                uuids = self._generate_layer_order(self.layers[layer])
                for uuid in uuids:
                    comp = self.components[uuid]
                    x = start_x+comp.get_width()/2
                    comp.draw(canvas, x, y)
                    start_x += comp.get_width() + 2*GRID_SIZE
            start_y += layer_heights[layer] + 2*GRID_SIZE

        # Draw Connections
        widths = []
        for layer in layer_widths:
            widths.append(layer_widths[layer])
        widest_layer = max(widths)

        surround_left_gap = GRID_SIZE*2
        surround_right_gap = GRID_SIZE*2

        connections_drawn = []
        for pair in self.pairs:
            if pair not in connections_drawn:
                comp_from = self.components[pair.comp_from_uuid]
                comp_to = self.components[pair.comp_to_uuid]
                x0, y0 = comp_from.get_output_coords(pair.comp_from_output)
                x_final, y_final = comp_to.get_input_coords(pair.comp_to_input)
                if pair.reverse:
                    if x0 <= middle_x:
                        x_wide = middle_x - widest_layer/2 - surround_left_gap
                        surround_left_gap += GRID_SIZE
                    else:
                        x_wide = middle_x + widest_layer/2 + surround_right_gap
                        surround_right_gap += GRID_SIZE
                    canvas.create_line(x0, y0, x0, y0 + GRID_SIZE)
                    canvas.create_line(x0, y0 + GRID_SIZE, x_wide, y0 + GRID_SIZE)
                    canvas.create_line(x_wide, y0 + GRID_SIZE, x_wide, y_final - GRID_SIZE)
                    canvas.create_line(x_wide, y_final - GRID_SIZE, x_final, y_final - GRID_SIZE)
                    canvas.create_line(x_final, y_final - GRID_SIZE, x_final, y_final, arrow=LAST)
                else:
                    canvas.create_line(x0, y0, x_final, y_final, arrow=LAST)
                connections_drawn.append(pair)

        self.canvas = canvas

    def save(self, filename):
        """ Saves the machine to filename as .eps and .png files. You must call .draw() first.
        
        Parameters
        ----------
        filename (str): The name of the file to save to
        
        Returns
        None
        """
        assert(self.canvas is not None)
        self.canvas.update()
        self.canvas.postscript(file=f'{filename}.eps')
        img = Image.open(f'{filename}.eps')
        img.save(f'{filename}.png', 'png')