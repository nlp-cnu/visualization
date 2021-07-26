class Node:
    """
    Node object, creates a tree
    """

    def __init__(self, id, weight, c1=None, c2=None, parent_edge_width=None, parent_edge_color=None):
        """
        initialization for node object
        :param id: id of node - int
        :param weight: size of node - int
        :param c1: first child - node object
        :param c2: second child - node object
        :param parent_edge_width: edge width connecting to parent - int
        :param parent_edge_color: edge color connecting to parent - string hex code
        """
        self.id = id
        self.weight = weight
        self.c1 = c1
        self.c2 = c2
        self.parent_edge_width = parent_edge_width
        self.parent_edge_color = parent_edge_color

    def set_c1(self, child):
        """
        sets the first child of node
        :param child: Node Object
        :return: None
        """
        self.c1 = child

    def set_c2(self, child):
        """
        sets the second child of node
        :param child: Node Object
        :return: None
        """
        self.c2 = child

    def set_parent_edge_width(self, num):
        """
        sets parent edge width
        :param num: int
        :return: None
        """
        self.parent_edge_width = num

    def set_parent_edge_color(self, color):
        """
        sets parent edge color
        :param color: String, hex code
        :return: None
        """
        self.parent_edge_color = color

    def get_id(self):
        """
        getter for id
        :return: node id - int
        """
        return self.id

    def get_weight(self):
        """
        getter for weight
        :return: size of node - inr
        """
        return self.weight

    def get_c1(self):
        """
        getter for first child
        :return: first child of node - Node
        """
        return self.c1

    def get_c2(self):
        """
        getter for second child
        :return: second child of node - Node
        """
        return self.c2

    def get_parent_edge_width(self):
        """
        getter for parent edge width
        :return: edge width - int
        """
        return self.parent_edge_width

    def get_parent_edge_color(self):
        """
        getter for parent edge color
        :return: edge color - String hex code
        """
        return self.parent_edge_color

    def __repr__(self):
        """
        representation function, for debugging purposes
        :return: string format for Node object
        """
        return "ID: {}, Width: {}, C1: {}, C2: {}".format(self.id, self.parent_edge_width, self.c1,
                                                          self.c2)
