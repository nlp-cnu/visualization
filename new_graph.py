import py4cytoscape as p4c
import node as ne
import pandas as pd
import codecs
import time
import re
import os

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
    #nodes.at[len(nodes['id'].tolist()) - 1, 'name'] = 'root'  # change name of root for clearness
    root = nodes.at[0, 'name']
    #nodes.at[0, 'name'] = 'root'  # change name of root for clearness


    # must be strings for cytoscape to read them in
    edges['source'] = edges['parent'].astype(str)
    edges['target'] = edges['child'].astype(str)

    print(nodes)
    print(edges)

    p4c.create_network_from_data_frames(nodes, edges, title=project_name, collection="Graphs")
    p4c.toggle_graphics_details()
    p4c.set_node_shape_default('ELLIPSE')  # default shape of ALL nodes - except root
    p4c.set_node_color_default('#00FF00')  # color should NOT appear
    p4c.set_node_size_mapping('id', nodes['id'].tolist(), nodes['size'].tolist(), mapping_type='d')
    p4c.set_node_font_size_mapping('id', nodes['id'].tolist(), nodes['font'].tolist(), mapping_type='d')
    p4c.set_edge_line_width_bypass(edges['name'].tolist(), edges['width'].tolist())
    p4c.set_edge_color_bypass(edges['name'].tolist(), edges['color'].tolist())
    p4c.set_node_shape_bypass([root], 'HEXAGON')  # root becomes hexagon
    p4c.set_node_color_bypass([root], '#FF0000')  # root becomes red
    #nodes.at[0, 'name'] = root  # restore root name

    end = time.time()  # end timer

    # timer information
    print("time taken in seconds:", end - start)
    print("time in minutes:", (end - start) / 60)


if __name__ == "__main__":
    # project = 'data/' + input("Please enter the name of your files without the extension, case sensitive. (ex -"
    #                           "cardiacArrestDiseases): ")
    project = 'data/test'
    graph_to_cytoscape(project)