import math
import os

if __name__ == '__main__':
    ontology = input("Please enter the ontology to graph: ")

    ontology_file = os.path.join("..","research_data" ,ontology+".txt")
    hierarchy_file = os.path.join("..","research_data" , ontology+"_HIER.txt")
    # AUIs = AUI, name, CUI, parent node, hierarchy, children, empty string (meant for descendants), ID
    AUIs = {}

    with open(ontology_file,encoding="utf-8") as f:
        ontology_lines = f.readlines()
        for line_num in range(len(ontology_lines)):
            ontology_lines[line_num] = ontology_lines[line_num].strip().split("|")
            AUIs[ontology_lines[line_num][7]] = [ontology_lines[line_num][7],ontology_lines[line_num][14], ontology_lines[line_num][0]]


    with open(hierarchy_file) as f:
        hier_lines = f.readlines()
        for line_num in range(len(hier_lines)):
            hier_lines[line_num] = hier_lines[line_num].strip().split("|")
            if(len(hier_lines[line_num][6]) > 1):
                root_AUI = hier_lines[line_num][6].split(".")
                root_AUI = root_AUI[0]
            if hier_lines[line_num][1] != root_AUI and hier_lines[line_num][2] == '1':
                AUIs[hier_lines[line_num][1]].append(hier_lines[line_num][3])
                AUIs[hier_lines[line_num][1]].append(hier_lines[line_num][6])
            elif hier_lines[line_num][1] == root_AUI:
                if root_AUI in AUIs.keys():
                    AUIs[hier_lines[line_num][1]].append(hier_lines[line_num][3])
                    AUIs[hier_lines[line_num][1]].append(hier_lines[line_num][6])
                else:
                    AUIs[root_AUI] = [root_AUI, "root", "NONE", "", '']

    #Set IDs
    index = 0
    for key, value in AUIs.items():
        if len(AUIs[key]) > 3:
            AUIs[key].append("")
            AUIs[key].append(index)
            index += 1

    #set size and get rid of commas in names
    for key, value in AUIs.items():
        if len(AUIs[key]) > 3:
            name = AUIs[key][1].replace(',','')
            AUIs[key][1] = name
            if AUIs[key][4] == '':
                AUIs[key].append(1)
                root = key
            else:
                AUIs[key].append(len(AUIs[key][4].split(".")) + 1)
    #print(AUIs['A1199224'])
    width = 100
    color = '#FFC0CB'
    file = os.path.join("..", "research_data" ,ontology+"_nodes.csv")
    with open(file, "wt") as f:
        f.write("id,name,size,aui\n")
        for key, value in AUIs.items():
            if len(AUIs[key]) > 3:
                size = 2000/(math.sqrt( AUIs[key][-1]))
                f.write("{},{},{},{}\n".format(AUIs[key][6],AUIs[key][1],int(size//1),key))

    file = os.path.join("..","research_data" , ontology+"_edges.csv")
    with open(file, "wt") as f:
        f.write("source,target,width,color,name\n")
        for key, value in AUIs.items():
            if len(AUIs[key]) > 3 and key != root:
                parent = AUIs[AUIs[key][3]][6]
                child = AUIs[key][6]
                f.write("{},{},{},{},{} (interacts with) {}\n".format(parent, child, width, color,parent, child))
            elif key == root:
                parent = -1
                child = AUIs[key][6]
                f.write("{},{},{},{},{} (interacts with) {}\n".format(parent, child, width, color, parent, child))
    # project = 'data/' + ontology
    # new_graph.graph_to_cytoscape(project)