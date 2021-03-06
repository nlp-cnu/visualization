# Interactive Graph Visualization for Literature Based Discovery
This program, specifically 'create_graph.py" will convert data from a literature based discovery (LBD) system straight to the Cytoscape program and create a fully interactive graph that provides easier means of exploring the data. Edges will be color coded, **blue** *for the more interesting child*, **orange** *for least interesting*, and **pink** *for equally interesting*. When the program is finished running, a layout must be chosen from the Cytoscape set choices, or even downloadable ones like the yFiles layouts.  

## Requirements:
[Cytoscape](https://cytoscape.org/)  
[yFiles layouts](https://apps.cytoscape.org/apps/yfileslayoutalgorithms) (for extra, more informative layouts)  
Correct LBD output, reference in instructions.

## Demo:
After downloading all files and required programs, open Cytoscape and run create_graph.py and enter "*demo*"  
Once the graph has been created, head over to the layout tab and experiment with different options - the [yFiles](https://apps.cytoscape.org/apps/yfileslayoutalgorithms) are quite useful.  
Click and drag through the graph at your pleasure and explore at your leisure

## Instructions for user data:
TODO - this format is overly complex, and specific to the original clustering algorithm and implementation. It should be a .node and a .edge file. Nodes should be able to have any ID, and the edge file should just contain node-node pairs to specify edges - probably also a weight to go along with the edge.

**1.** Verify you have the correct data from the LBD system - this is a: ".tree" and a ".clusters" file with the same name.  
   The structure of the tree is specified in a .tree and a .clusters file. The .tree file contains ege information and the .clusters file contains node information. Assign each node a unique ID between 0 and the number of nodes. Then, create the .tree and .clusters files as described below:

   The .tree file should be structured as the following... 
   
   >4957 0.000000e+00 0.000000e+00  
   >3888 0.000000e+00 0.000000e+00  
   >5062 0.000000e+00 0.000000e+00    
   
   Where the line number indicates the current node, and the first value on the line indictes that node's parent. For example, if line 0 contains the value 4957, it indicates that node 0's parent is 4957. A value of -1 indicates no parent node.
  
   The .cluster file should be structured as the following...  
  
   >3049 - local anesthetic throat preparations - 549: C3540696, C3540789,  
   >1485 - Recombinant Lymphokine - 286: C1527201,   
   >4736 - Guanidines - 1315: C0120447, C0041942, C0120446, C0018320,  

   Where, the first value indicates the ID of the node (0-number of nodes). The next value indicates the name of the node, the next value indictes the score of the node. This is followed by a list of values which indicates the contents of the node. In the case where a node represents a single concept, just a single value should appear after the colon.
  
 **2.** Open Cytoscape, must be open for graph to be created.  
 **3.** Run the create_graph.py and enter name of project files - both the tree and cluster file should have the same name.  
 **4.** Choose a layout from the many options - preferred are yFiles *circular and tree*  
 **5.** Explore the newly created graph and add changes of your own to personalize it to your project.  
 
 ## Example Graphs
 ![CytoscapeCircular](https://user-images.githubusercontent.com/58955553/126950513-ec6cbbc6-8891-43fa-beb6-dbf11dbffc30.png)
 ![CytoscapeTree](https://user-images.githubusercontent.com/58955553/126950988-611bfc80-4bfc-4d49-8851-514d2843a300.png)

