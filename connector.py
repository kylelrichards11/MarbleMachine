from statistics import mean

from tkinter import *
from PIL import Image
import io

from components import BlackBox

GRID_SIZE = 25

def save(canvas):
    canvas.update()
    canvas.postscript(file='image.eps')
    img = Image.open('image.eps')
    img.save('image.png', 'png')

def create_canvas(root, width, height):
    frame = Frame(root, width=width, height=height)
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

class Connection:
    def __init__(self, el_from, el_to, el_from_output=0, el_to_input=0, reverse=False):
        self.el_from = el_from
        self.el_to = el_to
        self.el_from_output = el_from_output
        self.el_to_input = el_to_input
        self.reverse = reverse

class SharedLayer:
    def __init__(self, el_left, el_right):
        self.el_left = el_left
        self.el_right = el_right

class Pair:
    def __init__(self, el_from_uuid, el_to_uuid, el_from_output, el_to_input, reverse):
        self.el_from_uuid = el_from_uuid
        self.el_to_uuid = el_to_uuid
        self.el_from_output = el_from_output
        self.el_to_input = el_to_input
        self.reverse = reverse

    def __str__(self):
        return f"From: {self.el_from_uuid}, To: {self.el_to_uuid}, From Output: {self.el_from_output}, To Input: {self.el_to_input}, Reverse: {self.reverse}"

class Connector:
    def __init__(self, root=None):
        self.root = root
        self.elements = {}
        self.layers = {}
        self.el_layers = {}
        self.pairs = []
        self.uuid_counter = 0
        self.black_boxes_added = []
        self.shared_layers = {}
        self.shared_layer_orders = {}

    def _add_to_layers(self, uuid, layer):
        if layer in self.layers:
            self.layers[layer].append(uuid)
        else:
            self.layers[layer] = [uuid]
        self.el_layers[uuid] = layer

    def _change_layer(self, uuid, new_layer, old_layer):
        if new_layer != old_layer:
            self.layers[old_layer].remove(uuid)
            self._add_to_layers(uuid, new_layer)
            # Change shared layer elements
            if uuid in self.shared_layers:
                for shared_el in self.shared_layers[uuid]:
                    if shared_el in self.el_layers:
                        self._change_layer(shared_el, new_layer, self.el_layers[shared_el])
            # Change future elements
            for pair in self.pairs:
                if pair.el_from_uuid == uuid:
                    if pair.el_to_uuid in self.el_layers:
                        self._change_layer(pair.el_to_uuid, new_layer+1, self.el_layers[pair.el_to_uuid])

    def add_shared_layer(self, layer):
        el_left_uuid = layer.el_left.get_uuid()
        el_right_uuid = layer.el_right.get_uuid()
        if el_left_uuid in self.shared_layers:
            self.shared_layers[el_left_uuid].append(el_right_uuid)
        else:
            self.shared_layers[el_left_uuid] = [el_right_uuid]
        if el_right_uuid in self.shared_layers:
            self.shared_layers[el_right_uuid].append(el_left_uuid)
        else:
            self.shared_layers[el_right_uuid] = [el_left_uuid]
        if el_right_uuid in self.shared_layer_orders:
            self.shared_layer_orders[el_right_uuid].append(el_left_uuid)
        else:
            self.shared_layer_orders[el_right_uuid] = [el_left_uuid]

    def add_element(self, el):
        if isinstance(el, BlackBox):
            self.add_black_box(el)
        else:
            self.add_component(el)

    def add_black_box(self, el):
        if el.get_uuid() not in self.black_boxes_added:
            self._create_uuid(el)
            self.black_boxes_added.append(el.get_uuid())
            self.elements[el.get_uuid()] = el
            for connection in el.get_connections():
                self.add_element(connection.el_from)
                self.add_element(connection.el_to)
            for shared_layer in el.get_shared_layers():
                self.add_shared_layer(shared_layer)

    def add_component(self, el):
        if el.get_uuid() == -1:
            self._create_uuid(el)
            self.elements[el.get_uuid()] = el

    def connect_black_box(self, el_from, el_to, el_from_output, el_to_input, reverse):
        self.add_element(el_from)
        self.add_element(el_to)
        
        if isinstance(el_from, BlackBox) and isinstance(el_to, BlackBox):
            for connection in el_from.get_connections():
                self.connect(connection)
            self.connect(Connection(
                el_from.outputs[el_from_output][0], 
                el_to.inputs[el_to_input][0], 
                el_to_input=el_to.inputs[el_to_input][1], 
                el_from_output=el_from.outputs[el_from_output][1])
            )
            for connection in el_to.get_connections():
                self.connect(connection)
        elif isinstance(el_from, BlackBox):
            for connection in el_from.get_connections():
                self.connect(connection)
            self.connect(Connection(
                el_from.outputs[el_from_output][0], 
                el_to, 
                el_to_input=el_to_input, 
                el_from_output=el_from.outputs[el_from_output][1])
            )
        else:
            self.connect(Connection(
                el_from, 
                el_to.inputs[el_to_input][0], 
                el_to_input=el_to.inputs[el_to_input][1], 
                el_from_output=el_from_output)
            )
            for connection in el_to.get_connections():
                self.connect(connection)

    def get_shared_layer(self, uuid, new_layer):
        shared_layer = new_layer
        for shared_el in self.shared_layers[uuid]:
            if shared_el in self.el_layers:
                if new_layer > self.el_layers[shared_el]:
                    self._change_layer(shared_el, new_layer, self.el_layers[shared_el])
                shared_layer = self.el_layers[shared_el]
        return shared_layer

    def create_layers(self):
        for pair in self.pairs:
            from_uuid = pair.el_from_uuid
            to_uuid = pair.el_to_uuid
            if from_uuid in self.el_layers and to_uuid in self.el_layers:
                if self.el_layers[to_uuid] <= self.el_layers[from_uuid]:
                    if not pair.reverse:
                        self._change_layer(to_uuid, self.el_layers[from_uuid] + 1, self.el_layers[to_uuid])
            elif from_uuid in self.el_layers:
                new_layer = self.el_layers[from_uuid] + 1
                if to_uuid in self.shared_layers:
                    new_layer = self.get_shared_layer(to_uuid, new_layer)
                self._add_to_layers(to_uuid, new_layer)
            elif to_uuid in self.el_layers:
                new_layer = self.el_layers[to_uuid] - 1
                if from_uuid in self.shared_layers:
                    new_layer = self.get_shared_layer(from_uuid, new_layer)
                self._add_to_layers(from_uuid, new_layer)
            else:
                new_layer_from = 0
                if from_uuid in self.shared_layers:
                    new_layer_from = self.get_shared_layer(from_uuid, new_layer_from)
                self._add_to_layers(from_uuid, new_layer_from)

                new_layer_to = 1
                if to_uuid in self.shared_layers:
                    new_layer_to = self.get_shared_layer(to_uuid, new_layer_to)
                self._add_to_layers(to_uuid, new_layer_to)
            
    def connect_component(self, el_from, el_to, el_from_output, el_to_input, reverse):
        self.add_component(el_from)
        self.add_component(el_to)

        from_uuid = el_from.get_uuid()
        to_uuid = el_to.get_uuid()

        self.pairs.append(Pair(from_uuid, to_uuid, el_from_output, el_to_input, reverse))

    def connect(self, con):
        if (isinstance(con.el_from, BlackBox) and con.el_from.show_all) or (isinstance(con.el_to, BlackBox) and con.el_to.show_all):
            self.connect_black_box(con.el_from, con.el_to, con.el_from_output, con.el_to_input, con.reverse)
        else:
            self.connect_component(con.el_from, con.el_to, con.el_from_output, con.el_to_input, con.reverse)

    def _create_uuid(self, el):
        assert(el.get_uuid() == -1)
        el.assign_uuid(self.uuid_counter)
        self.uuid_counter += 1

    def get_layer_widths(self):
        widths = {}
        for layer in self.layers:
            width = 0
            for uuid in self.layers[layer]:
                el = self.elements[uuid]
                width += el.get_width()
                width += 2*GRID_SIZE
            width -= 2*GRID_SIZE
            widths[layer] = width
        return widths

    def get_layer_heights(self):
        heights = {}
        for layer in self.layers:
            height = 0
            for uuid in self.layers[layer]:
                el = self.elements[uuid]
                height = max(height, el.get_height())
            heights[layer] = height
        return heights

    def calc_total_size(self):
        widths = self.get_layer_widths()
        heights = self.get_layer_heights()
        
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

    def _get_canvas_dims(self):
        total_width, total_height = self.calc_total_size()
        canv_width = total_width + 2*GRID_SIZE
        canv_height = total_height + 2*GRID_SIZE
        return canv_height, canv_width

    def generate_layer_order(self, orig_layer_uuids):
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
            

    def draw(self, canvas=None, x=-1, y=-1):

        # Assign Layers
        self.create_layers()

        # Define Canvas
        if canvas is None:
            canv_width, canv_height = self._get_canvas_dims()
            assert(self.root is not None)
            canvas = create_canvas(self.root, 1500, 2000)
            middle_x = canv_width/2
            start_y = 2*GRID_SIZE
        else:
            _, total_height = self.calc_total_size()
            middle_x = x
            start_y = y - total_height/2 - 2*GRID_SIZE

        layer_widths = self.get_layer_widths()
        layer_heights = self.get_layer_heights()

        # Draw Layers
        for layer in sorted(self.layers.keys()):
            start_x = middle_x - layer_widths[layer]/2
            y = start_y + layer_heights[layer]/2
            if len(self.layers[layer]) == 1 and layer != sorted(self.layers.keys())[0]:
                uuid = self.layers[layer][0]
                el = self.elements[uuid]
                prev_output_xs = []
                for pair in self.pairs:
                    if pair.el_to_uuid == uuid and not pair.reverse:
                        prev_output_xs.append(self.elements[pair.el_from_uuid].get_output_coords(pair.el_from_output)[0])
                avg_x = mean(prev_output_xs)
                el.draw(canvas, avg_x, y)
            else:
                uuids = self.generate_layer_order(self.layers[layer])
                for uuid in uuids:
                    el = self.elements[uuid]
                    x = start_x+el.get_width()/2
                    el.draw(canvas, x, y)
                    start_x += el.get_width() + 2*GRID_SIZE
            start_y += layer_heights[layer] + 2*GRID_SIZE

        widths = []
        for layer in layer_widths:
            widths.append(layer_widths[layer])
        widest_layer = max(widths)

        # Draw Connections
        for pair in self.pairs:
            el_from = self.elements[pair.el_from_uuid]
            el_to = self.elements[pair.el_to_uuid]
            x0, y0 = el_from.get_output_coords(pair.el_from_output)
            x_final, y_final = el_to.get_input_coords(pair.el_to_input)
            if pair.reverse:
                if x0 <= middle_x:
                    x_wide = middle_x - widest_layer/2 - GRID_SIZE*2
                else:
                    x_wide = middle_x + widest_layer/2 + GRID_SIZE*2
                canvas.create_line(x0, y0, x0, y0 + GRID_SIZE)
                canvas.create_line(x0, y0 + GRID_SIZE, x_wide, y0 + GRID_SIZE)
                canvas.create_line(x_wide, y0 + GRID_SIZE, x_wide, y_final - GRID_SIZE)
                canvas.create_line(x_wide, y_final - GRID_SIZE, x_final, y_final - GRID_SIZE, arrow=LAST)
                canvas.create_line(x_final, y_final - GRID_SIZE, x_final, y_final)
            else:
                canvas.create_line(x0, y0, x_final, y_final, arrow=LAST)