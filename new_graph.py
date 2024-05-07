import py4cytoscape as p4c
import node as ne
import pandas as pd
#import codecs
import time
import re
import os
import csv

def graph_to_cytoscape(project_name):
    """

    :param project_name:
    :return:
    """

    start = time.time()  # tracking time for user purposes



    line_num = 0
    with open(project_name + '_nodes.csv', "r") as file:
        for line in file:
            if line_num==2784:
                print(line)
            if line_num==2785:
                print(line)
            if line_num==2786:
                print(line)
            line_num += 1
    #exit()
         

    
    nodes = pd.read_csv(project_name + '_nodes.csv', sep='\t', quoting=csv.QUOTE_NONE)
    # #
    # edges = pd.read_csv(project_name + '_edges.csv', sep='\t', quoting=csv.QUOTE_NONE)



    # read the nodes file
    with open(project_name + '_nodes.csv', "r") as file:
        # create the nodes dictionary
        nodes= {}

        # read the label row (row the containing the labels for each column)
        titles = file.readline().strip('\n').split()
        nodes[titles[0]] = []
        nodes[titles[1]] = []
        nodes[titles[2]] = []
        nodes[titles[3]] = []
        nodes[titles[4]] = []
        nodes[titles[5]] = []
        nodes[titles[6]] = []
        nodes[titles[7]] = []
        print(titles)

        reader = csv.reader(file, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE)
        for row in reader:
            size = 100
            if row[3] == "Prescription" or row[3] == "OTC":
                 size=300
            nodes.get(titles[0]).append(int(row[0]))
            nodes.get(titles[1]).append(row[1])
            nodes.get(titles[2]).append(size)
            nodes.get(titles[3]).append(row[3])
            nodes.get(titles[4]).append(row[4])
            nodes.get(titles[5]).append(row[5])
            nodes.get(titles[6]).append(row[6])
            nodes.get(titles[7]).append(row[7])




    with open(project_name + '_edges.csv', "r") as file:
        count = 0
        edges= {}
        titles = file.readline().strip('\n').split('\t')
        print(titles)
        edges[titles[0]] = []
        edges["target"] = []
        edges[titles[2]] = []
        edges[titles[3]] = []
        edges[titles[4]] = []
        edges[titles[5]] = []
        edges[titles[6]] = []
        reader = csv.reader(file, delimiter='\t',lineterminator='\n', quoting=csv.QUOTE_NONE)
        for row in reader:
            edges.get(titles[0]).append(int(row[0]))
            edges.get("target").append(int(row[1]))
            edges.get(titles[2]).append(int(row[2]))
            edges.get(titles[3]).append(row[3])
            edges.get(titles[4]).append(row[4])
            edges.get(titles[5]).append(row[5])
            edges.get(titles[6]).append(row[6])

            count += 1

    nodes = pd.DataFrame.from_dict(nodes)
    edges = pd.DataFrame.from_dict(edges)
    print("STOP")
    print(edges)
    print(nodes)



    #nodes['id'] = nodes.astype(str)
    #
    nodes['font'] = nodes['size'].map(lambda x: 32767 if x / 5 > 32767 else x / 5)  # font sizes -> scale factor here
    #nodes.at[len(nodes['id'].tolist()) - 1, 'name'] = 'root'  # change name of root for clearness
    counter = -1
    root_id = None
    root_index = 0
    for s in edges['source']:
        counter += 1
        if s == -1:
            root_id = edges.target[counter]
            edges = edges.drop(edges.index[counter])
    counter = -1
    for node in nodes['id']:
        counter += 1
        if node == root_id:
            root_index = counter
    root = nodes.at[root_index, 'name']
    print(root)
    #nodes.at[0, 'name'] = 'root'  # change name of root for clearness



    # must be strings for cytoscape to read them in
    edges['source'] = edges['source'].astype(str)
    edges['target'] = edges['target'].astype(str)
    nodes['id'] = nodes['id'].astype(str)



    p4c.create_network_from_data_frames(nodes, edges, title=project_name, collection="DailyMedGraph")
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

    project = '../data/' + input("Please enter the name of your files without the extension, case sensitive. (ex - cardiacArrestDiseases): ")
    #project = 'data/SNOMEDCT_US'
    #project = '/home/kelsey/visualization/sample_data/'+ input("Please enter the name of your files without the extension, case sensitive. (ex - cardiacArrestDiseases):")
    graph_to_cytoscape(project)

