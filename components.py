from shapes import Rectangle, Circle, Diamond, Star

GRID_SIZE = 25

##############################################################################################################################
class Sorter:
    def __init__(self, outputs):
        self.outputs = outputs
        self.height = 3*GRID_SIZE
        assert(len(outputs) > 0)
        output_spaces = len(outputs) - 1
        total_outputs = 0
        for output in outputs:
            total_outputs += len(output)
        self.width = max(self.height, (total_outputs + output_spaces)*GRID_SIZE)
        self.uuid = -1
        self.x = -1
        self.y = -1
    
    def draw(self, canvas, x, y):
        self.x = x
        self.y = y
        Rectangle(self.height, self.width).draw(canvas, x, y)
        left_x = x - self.width/2
        output_x = GRID_SIZE/2
        output_y = y + GRID_SIZE
        for output in self.outputs:
            for out in output:
                Circle(GRID_SIZE/2, edge_color=out).draw(canvas, left_x+output_x, output_y)
                output_x += GRID_SIZE
            output_x += GRID_SIZE

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def assign_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def get_input_coords(self, input_num):
        assert(self.x > -1)
        assert(self.y > -1)
        return self.x, self.y - self.height/2

    def get_output_coords(self, output_num):
        assert(self.x > -1)
        assert(self.y > -1)
        i = 0
        offset = 0
        while i < output_num:
            offset += len(self.outputs[i])*GRID_SIZE
            offset += GRID_SIZE
            i += 1
        x = self.x - self.width/2 + offset + len(self.outputs[output_num])*GRID_SIZE/2
        y = self.y + self.height/2
        return x, y
            
##############################################################################################################################
class Replacer:
    def __init__(self, inputs, outputs):
        assert(len(inputs) > 0)
        assert(len(outputs) > 0)
        self.inputs = inputs
        self.outputs = outputs
        self.width = (3 + max(len(inputs), len(outputs)))*GRID_SIZE
        self.uuid = -1
        self.x = -1
        self.y = -1

    def draw(self, canvas, x, y):
        self.x = x
        self.y = y
        Diamond(self.width).draw(canvas, x, y)

        max_len = max(len(self.inputs), len(self.outputs))
        
        input_left_x = x - (len(self.inputs) - 1)*GRID_SIZE/2
        input_x = 0
        input_y = y - GRID_SIZE - (max_len - len(self.inputs))*GRID_SIZE/2
        
        output_left_x = x - (len(self.outputs) - 1)*GRID_SIZE/2
        output_x = 0
        output_y = y + GRID_SIZE + (max_len - len(self.outputs))*GRID_SIZE/2

        
        for input in self.inputs:
            if input == 'all':
                Circle(GRID_SIZE/2).draw(canvas, input_left_x + input_x, input_y)
                Star(GRID_SIZE).draw(canvas, input_left_x + input_x, input_y)
            else:
                Circle(GRID_SIZE/2, edge_color=input).draw(canvas, input_left_x + input_x, input_y)
            input_x += GRID_SIZE

        for output in self.outputs:
            Circle(GRID_SIZE/2, edge_color=output).draw(canvas, output_left_x + output_x, output_y)
            output_x += GRID_SIZE

    def get_width(self):
        return self.width

    def get_height(self):
        return self.width

    def assign_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def get_input_coords(self, input_num):
        assert(self.x > -1)
        assert(self.y > -1)
        return self.x, self.y - self.width/2

    def get_output_coords(self, output_num):
        assert(self.x > -1)
        assert(self.y > -1)
        return self.x, self.y + self.width/2
    
##############################################################################################################################
class IO:
    def __init__(self, balls=[]):
        self.balls = balls
        self.uuid = -1
        self.x = -1
        self.y = -1

    def draw(self, canvas, x, y):
        self.x = x
        self.y = y
        Circle(2*GRID_SIZE).draw(canvas, x, y)
        ball_x = x
        ball_y = y + 2*GRID_SIZE - GRID_SIZE/2
        for ball in self.balls:
            Circle(GRID_SIZE/2, ball, ball).draw(canvas, ball_x, ball_y)

    def get_width(self):
        return 4*GRID_SIZE

    def get_height(self):
        return 4*GRID_SIZE

    def assign_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def get_input_coords(self, input_num):
        assert(self.x > -1)
        assert(self.y > -1)
        return self.x, self.y - 2*GRID_SIZE

    def get_output_coords(self, output_num):
        assert(self.x > -1)
        assert(self.y > -1)
        return self.x, self.y + 2*GRID_SIZE

##############################################################################################################################
class BlackBox:
    def __init__(self, show_all=False):
        self.show_all = show_all
        self.uuid = -1
        self.x = -1
        self.y = -1
        self.shared_layers = []

    def draw(self, canvas, x, y, show_all=False):
        self.x = x
        self.y = y
        if not self.show_all:
            Rectangle(3*GRID_SIZE, 3*GRID_SIZE, fill_color='black').draw(canvas, x, y)
            canvas.create_text(x, y, fill='white', text=self.name)

    def get_width(self):
        assert(not self.show_all)
        return 3*GRID_SIZE

    def get_height(self):
        assert(not self.show_all)
        return 3*GRID_SIZE

    def assign_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def get_input_coords(self, input_num):
        assert(self.x > -1)
        assert(self.y > -1)
        if self.show_all:
            return self.inputs[input_num].get_input_coords()
        num_inputs = len(self.inputs)
        input_spacing = self.get_width()/(num_inputs + 1)
        left_x = self.x - self.get_width()/2
        return left_x + (input_num+1)*input_spacing, self.y - 1.5*GRID_SIZE

    def get_output_coords(self, output_num):
        assert(self.x > -1)
        assert(self.y > -1)
        if self.show_all:
            return self.outputs[output_num].get_output_coords()
        num_outputs = len(self.outputs)
        output_spacing = self.get_width()/(num_outputs + 1)
        left_x = self.x - self.get_width()/2
        return left_x + (output_num+1)*output_spacing, self.y + 1.5*GRID_SIZE

    def get_connections(self):
        return self.connections

    def get_shared_layers(self):
        return self.shared_layers