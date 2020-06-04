class Circle:
    def __init__(self, radius, edge_color=None, fill_color=None):
        self.radius = radius
        self.edge_color = edge_color
        self.fill_color = fill_color

    def draw(self, canvas, x, y):
        x0 = x - self.radius
        y0 = y - self.radius
        x1 = x + self.radius
        y1 = y + self.radius
        canvas.create_oval(x0, y0, x1, y1, outline=self.edge_color, fill=self.fill_color)

class Rectangle:
    def __init__(self, height, width, fill_color=None):
        self.height = height
        self.width = width
        self.fill_color = fill_color

    def draw(self, canvas, x, y):
        x0 = x - self.width/2
        y0 = y - self.height/2
        x1 = x + self.width/2
        y1 = y + self.height/2
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.fill_color)

class Diamond:
    def __init__(self, width):
        self.width = width

    def draw(self, canvas, x, y):
        half_width = self.width/2
        canvas.create_line(x - half_width, y, x, y + half_width)
        canvas.create_line(x + half_width, y, x, y + half_width)
        canvas.create_line(x - half_width, y, x, y - half_width)
        canvas.create_line(x + half_width, y, x, y - half_width)

class Star:
    def __init__(self, size):
        self.size = size

    def draw(self, canvas, x, y):
        space = self.size/5

        canvas.create_line(x - 2*self.size/5, y - self.size/10, x + 2*self.size/5, y - self.size/10)
        canvas.create_line(x, y - 2*self.size/5, x + self.size/4, y + 2*self.size/5)
        canvas.create_line(x + 2*self.size/5, y - self.size/10, x - self.size/4, y + 2*self.size/5)
        canvas.create_line(x + self.size/4, y + 2*self.size/5, x - 2*self.size/5, y - self.size/10)
        canvas.create_line(x - self.size/4, y + 2*self.size/5, x, y - 2*self.size/5)