"""
@author Rafael Diaz
@date 07/26/2021
"""
import py4cytoscape as p4c
import node as ne
import pandas as pd
import codecs
import time
import re
import os


def tree_to_txt(tree):
    """
    converts .tree to .txt with " " delimiter
    :param tree: name of the file with no extension, MUST BE A ".tree" file
    :return: none -> creates new file
    """
    with open(tree + '.tree') as file:
        wrt = open(tree + '_edges.csv', 'w')
        lines = file.readlines()
        wrt.writelines(lines)
        wrt.close()


def clusters_to_csv(clusters):
    """
    converts .clusters to .csv with "\t" delimiter
    :param clusters: name of file with no extension, MUST BE A ".clusters" file
    :return: none -> creates new file
    """
    block_size = 1048576
    with codecs.open(clusters + '.clusters', "r", "windows-1252") as sourceFile:
        with codecs.open('data/dump.txt', "w", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(block_size)
                if not contents:
                    break
                targetFile.write(contents)
        targetFile.close()

    with open('data/dump.txt') as file:
        wrt = open(clusters + '_nodes.csv', 'w')
        for i in file:
            split_list = re.findall(r"(\d+) - (.*) - (\d+: .*)", i)[0]
            wrt.write(split_list[0] + "\t" + split_list[1] + "\t" + split_list[2] + "\n")
        wrt.close()

    os.remove('data/dump.txt')


def clean_data(project_name):
    """
    cleans most of the data by removing useless information and separating other information for ease of sizing
    :param project_name:
    :return:
    """
    # creating nodes panda dataframe
    nodes = pd.read_csv(project_name + '_nodes.csv', delimiter='\t', names=['id', 'name', 'size'])

    # separating size from UMLS information
    sizes = []
    umls_info = []

    for i in nodes['size']:
        sep = i.split(':')
        sizes.append(int(sep[0]))  # adding the size of node -> if scale, enter scale factor here
        umls_info.append(sep[1])  # UMLS associated information, example: C0016762

    nodes['size'] = pd.Series(sizes)
    nodes['info'] = pd.Series(umls_info)
    nodes = nodes.sort_values('id')

    # reading in the edges data frame
    edges = pd.read_csv(project_name + '_edges.csv', delimiter=' ', names=['source', 'n1', 'n2'])
    edges['target'] = edges.index  # adding index as an actual column

    # deleting useless information
    del edges['n1']
    del edges['n2']
    edges = edges[:-1]
    edges = edges.sort_values('source')

    # writing back into csv files to edit in other methods
    nodes.to_csv(project_name + '_nodes.csv')
    edges.to_csv(project_name + '_edges.csv')


def width_recurse(node):
    """
    traverses through a given node and creates edge weights for each edge -> edge size is sum of leaf nodes below
    :param node: given node object
    :return: no actual return - modifies actual tree
    """
    if node is None:  # base case
        return 0
    elif node.get_c1() is None and node.get_c2() is None:  # if node is a leaf node
        node.set_parent_edge_width(node.get_weight())
        return node.get_weight()
    elif node.get_c2() is None:  # if there is only one children
        num = width_recurse(node.get_c1())
        node.set_parent_edge_width(num)
        return num
    else:  # if there are two children
        num = width_recurse(node.get_c1()) + width_recurse(node.get_c2())
        node.set_parent_edge_width(num)
        return num


def edge_color_recurse(node):
    """

    :param node:
    :return:
    """
    color1 = '#0000FF'  # more interesting color
    color2 = '#FFA500'  # least interesting color
    color3 = '#FFC0CB'  # widths are the same
    if node is None or (node.get_c1() is None and node.get_c2() is None):  # base case, if not node or leaf node
        return 0
    elif node.get_c2() is None:  # if only one children, that should be the most interesting route
        node.get_c1().set_parent_edge_color(color1)
    else:
        if node.get_c1().get_parent_edge_width() > node.get_c2().get_parent_edge_width():  # C1 more interesting than C2
            node.get_c1().set_parent_edge_color(color1)
            node.get_c2().set_parent_edge_color(color2)
        elif node.get_c1().get_parent_edge_width() < node.get_c2().get_parent_edge_width():  # C2 > C1 in interest
            node.get_c2().set_parent_edge_color(color1)
            node.get_c1().set_parent_edge_color(color2)
        else:  # otherwise, if they are the same, give them their own color
            node.get_c1().set_parent_edge_color(color3)
            node.get_c2().set_parent_edge_color(color3)
        # continue recursion
        edge_color_recurse(node.get_c1())
        edge_color_recurse(node.get_c2())


def create_width(project_name):
    # open files
    nodes = pd.read_csv(project_name + '_nodes.csv')
    edges = pd.read_csv(project_name + '_edges.csv')

    node_id = nodes['id'].tolist()
    size = nodes['size'].tolist()

    all_nodes = {}  # make dict of all nodes, key is ID # and value is the actual node object
    for i in range(len(node_id)):
        all_nodes[node_id[i]] = (ne.Node(node_id[i], size[i]))

    source = edges['source'].tolist()
    target = edges['target'].tolist()

    # linking all nodes to each other
    for i in range(len(source)):
        if source[i] in all_nodes.keys() and target[i] in all_nodes.keys():  # verifying node is defined
            if all_nodes[source[i]].get_c1() is None:  # if a child has not been set, set as first
                all_nodes[source[i]].set_c1(all_nodes[target[i]])
            else:  # otherwise set as second child
                all_nodes[source[i]].set_c2(all_nodes[target[i]])
        else:
            quit("Source or target node not defined")

    # edge width section
    width_recurse(all_nodes[len(node_id) - 1])  # recurse through entire tree
    edge_widths = []
    for i in all_nodes.values():
        edge_widths.append(i.get_parent_edge_width() / 5)  # appending edge weight -> scale factor here
    edges = edges.sort_values('target')
    edges['width'] = edge_widths[:-1]  # removing unnecessary data

    # edge color section
    edge_color_recurse(all_nodes[len(node_id) - 1])  # recurse through entire tree
    colors = []
    for i in all_nodes.values():
        colors.append(i.get_parent_edge_color())
    edges['color'] = colors[:-1]

    # edge name section
    names = []
    for i in range(len(edges)):
        names.append(str(edges['source'][i]) + ' (interacts with) ' + str(edges['target'][i]))
    edges = edges.sort_values('source')
    edges['name'] = names
    edges.to_csv(project_name + '_edges.csv')


def graph_to_cytoscape(project_name):
    """

    :param project_name:
    :return:
    """
    start = time.time()  # tracking time for user purposes

    nodes = pd.read_csv(project_name + '_nodes.csv')
    edges = pd.read_csv(project_name + '_edges.csv')

    nodes['id'] = nodes.id.astype(str)
    nodes['font'] = nodes['size'].map(lambda x: 32767 if x / 3 > 32767 else x / 3)  # font sizes -> scale factor here
    nodes.at[len(nodes['id'].tolist()) - 1, 'name'] = 'root'  # change name of root for clearness

    # must be strings for cytoscape to read them in
    edges['source'] = edges['source'].astype(str)
    edges['target'] = edges['target'].astype(str)

    p4c.create_network_from_data_frames(nodes, edges, title="lbd_test", collection="tests")
    p4c.toggle_graphics_details()
    p4c.set_node_shape_default('ELLIPSE')  # default shape of ALL nodes - except root
    p4c.set_node_color_default('#00FF00')  # color should NOT appear
    p4c.set_node_size_mapping('id', nodes['id'].tolist(), nodes['size'].tolist(), mapping_type='d')
    p4c.set_node_font_size_mapping('id', nodes['id'].tolist(), nodes['font'].tolist(), mapping_type='d')
    p4c.set_edge_line_width_bypass(edges['name'].tolist(), edges['width'].tolist())
    p4c.set_edge_color_bypass(edges['name'].tolist(), edges['color'].tolist())
    p4c.set_node_shape_bypass(['root'], 'HEXAGON')  # root becomes hexagon
    p4c.set_node_color_bypass(['root'], '#FF0000')  # root becomes red

    end = time.time()  # end timer

    # timer information
    print("time taken in seconds:", end - start)
    print("time in minutes:", (end - start) / 60)


if __name__ == "__main__":
    project = 'data/' + input("Please enter the name of your files without the extension, case sensitive. (ex -"
                              "cardiacArrestDiseases): ")
    print('Processing...')
    clusters_to_csv(project)
    tree_to_txt(project)
    clean_data(project)
    create_width(project)
    print('Graphing...')
    graph_to_cytoscape(project)
