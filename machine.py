from statistics import mean

from tkinter import *
from PIL import Image
import io

from components import BlackBox, IO
from globals import GRID_SIZE, LAYER_GAP

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
        self.outputs = []
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
                total_height += LAYER_GAP
        total_height -= LAYER_GAP
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

    def _change_layer_edges(self, layer_edges, start_layer, end_layer, direction, edge):
        assert(direction == 'left' or direction == 'right')

        for layer in range(start_layer, end_layer+1):
            if direction == 'left':
                layer_edges[layer][direction] = edge - GRID_SIZE
            else:
                layer_edges[layer][direction] = edge + GRID_SIZE

        return layer_edges

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

        # Make sure outputs are alone in the last layer
        output_uuids = []
        for output in self.outputs:
            output_uuids.append(output.get_uuid())

        last_layer = max(self.layers.keys())
        make_layer = False
        for comp_uuid in self.layers[last_layer]:
            if comp_uuid not in output_uuids:
                make_layer = True
                break

        if make_layer:
            last_layer = last_layer + 1

        for comp_uuid in output_uuids:
            self._change_layer(comp_uuid, last_layer, self.comp_layers[comp_uuid])


    def _create_uuid(self, comp):
        assert(comp.get_uuid() == -1)
        comp.assign_uuid(self.uuid_counter)
        self.uuid_counter += 1
    
    def _detect_collisions(self, x0, y0, x1, y1):
        for comp_uuid in self.components:
            if self.components[comp_uuid].collides(x0, y0, x1, y1):
                return True
        return False

    def _draw_connection_around(self, canvas, middle_x, layer_edges, layer_horizontals, start_layer, end_layer, x0, y0, x_final, y_final, is_reverse):
        if not is_reverse:
            start_layer = start_layer + 1
            end_layer = end_layer - 1
        if start_layer > end_layer:
            temp_start = start_layer
            start_layer = end_layer
            end_layer = temp_start
        if x0 <= middle_x:
            direction = 'left'
            widest_edge = self._get_widest_layer_edge(layer_edges, start_layer, end_layer, direction) - GRID_SIZE
            layer_edges = self._change_layer_edges(layer_edges, start_layer, end_layer, direction, widest_edge)
        else:
            direction = 'right'
            widest_edge = self._get_widest_layer_edge(layer_edges, start_layer, end_layer, direction) + GRID_SIZE
            layer_edges = self._change_layer_edges(layer_edges, start_layer, end_layer, direction, widest_edge)
        above_y = 1/(layer_horizontals[end_layer]['above'][direction] + 1)*LAYER_GAP/2
        below_y = 1/(layer_horizontals[start_layer]['below'][direction] + 1)*LAYER_GAP/2
        layer_horizontals[end_layer]['above'][direction] += 1
        layer_horizontals[start_layer]['below'][direction] += 1
        canvas.create_line(x0, y0, x0, y0 + below_y)
        canvas.create_line(x0, y0 + below_y, widest_edge, y0 + below_y)
        canvas.create_line(widest_edge, y0 + below_y, widest_edge, y_final - above_y)
        canvas.create_line(widest_edge, y_final - above_y, x_final, y_final - above_y)
        canvas.create_line(x_final, y_final - above_y, x_final, y_final, arrow=LAST)
        return layer_edges

    def _draw_connections(self, canvas, middle_x):
        layer_widths = self._get_layer_widths()

        layer_edges = {}
        for layer in self.layers:
            layer_edges[layer] = {'left' : middle_x - layer_widths[layer]/2, 'right' : middle_x + layer_widths[layer]/2}

        layer_horizontals = {}
        for layer in self.layers:
            layer_horizontals[layer] = {'above' : {'left' : 0, 'right' : 0}, 'below' : {'left' : 0, 'right' : 0}}

        connections_drawn = []
        for pair in self.pairs:
            if pair not in connections_drawn:
                comp_from = self.components[pair.comp_from_uuid]
                comp_to = self.components[pair.comp_to_uuid]
                x0, y0 = comp_from.get_output_coords(pair.comp_from_output)
                x_final, y_final = comp_to.get_input_coords(pair.comp_to_input)
                if pair.reverse:
                    start_layer = self.comp_layers[pair.comp_from_uuid]
                    end_layer = self.comp_layers[pair.comp_to_uuid]
                    layer_edges = self._draw_connection_around(canvas, middle_x, layer_edges, layer_horizontals, start_layer, end_layer, x0, y0, x_final, y_final, True)
                else:
                    if self._detect_collisions(x0, y0, x_final, y_final):
                        start_layer = self.comp_layers[pair.comp_from_uuid]
                        end_layer = self.comp_layers[pair.comp_to_uuid]
                        layer_edges = self._draw_connection_around(canvas, middle_x, layer_edges, layer_horizontals, start_layer, end_layer, x0, y0, x_final, y_final, False)
                    else:
                        canvas.create_line(x0, y0, x_final, y_final, arrow=LAST)
                connections_drawn.append(pair)

    def _draw_layers(self, canvas, middle_x, start_y):
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
                if len(prev_output_xs) == 0:
                    avg_x = middle_x
                else:
                    avg_x = mean(prev_output_xs)
                comp.draw(canvas, avg_x, y)
            else:
                uuids = self._generate_layer_order(self.layers[layer])
                for uuid in uuids:
                    comp = self.components[uuid]
                    x = start_x+comp.get_width()/2
                    comp.draw(canvas, x, y)
                    start_x += comp.get_width() + LAYER_GAP
            start_y += layer_heights[layer] + LAYER_GAP

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
                width += LAYER_GAP
            width -= LAYER_GAP
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

    def _get_widest_layer_edge(self, layer_edges, start_layer, end_layer, direction):
        assert(direction == 'left' or direction == 'right')

        if direction == 'left':
            widest = 1000000
            for layer in range(start_layer, end_layer):
                widest = min(widest, layer_edges[layer][direction])
        else:
            widest = 0
            for layer in range(start_layer, end_layer):
                widest = max(widest, layer_edges[layer][direction])
        return widest

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
            canv_height = max(10000, canv_height)
            assert(self.root is not None)
            canvas = self._create_canvas(canv_width, canv_height)
            middle_x = canv_width/2 + 200
            start_y = LAYER_GAP
        else:
            assert(x > 0)
            assert(y > 0)
            _, total_height = self._calc_total_size()
            middle_x = x
            start_y = y - total_height/2 - LAYER_GAP

        self._draw_layers(canvas, middle_x, start_y)
        self._draw_connections(canvas, middle_x)
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

    def specify_output(self, io_comp):
        """ Specifies a component as an output IO to the machine. This allows it to make sure that all the outputs are in the last layer

        Parameters
        ----------
        io_comp (IO): The component to specify as an output

        Returns
        -------

        None
        """
        assert(isinstance(io_comp, IO))
        self.outputs.append(io_comp)