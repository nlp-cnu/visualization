class Node:

    def __init__(self, id, weight, c1=None, c2=None, parent_edge_width=None, parent_edge_color=None):
        self.id = id
        self.weight = weight
        self.c1 = c1
        self.c2 = c2
        self.parent_edge_width = parent_edge_width
        self.parent_edge_color = parent_edge_color

    def set_c1(self, child):
        self.c1 = child

    def set_c2(self, child):
        self.c2 = child

    def set_parent_edge_width(self, num):
        self.parent_edge_width = num

    def set_parent_edge_color(self, num):
        self.parent_edge_color = num

    def get_id(self):
        return self.id

    def get_weight(self):
        return self.weight

    def get_c1(self):
        return self.c1

    def get_c2(self):
        return self.c2

    def get_parent_edge_width(self):
        return self.parent_edge_width

    def get_parent_edge_color(self):
        return self.parent_edge_color

    def __repr__(self):
        return "ID: {}, Width: {}, C1: {}, C2: {}".format(self.id, self.parent_edge_width, self.c1,
                                                          self.c2)


class Edge:

    def __init__(self, parent, child, width=None):
        self.parent = parent
        self.child = child
        self.width = width

    def set_width(self, width):
        self.width = width

    def get_parent(self):
        return self.parent

    def get_child(self):
        return self.child

    def get_width(self):
        return self.width

    def __repr__(self):
        return "filled"
        # return "Parent: {}, Child: {}, Width: {}".format(self.parent, self.child, self.width)