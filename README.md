# Interactive Graph Visualization for Literature Based Discovery
This program will convert data from a literature based discovery (LBD) system straight to the Cytoscape program and create a fully interactive graph that provides easier means of exploring this data.
<h2>Requirements:</h2>
<a href="https://cytoscape.org/">Cytoscape</a><br />
Correct LBD output, reference in instructions.
<h2>Instructions:</h2>
1. Verify you have the correct data from the LBD system - this is a: ".tree" and a ".clusters" file with the same name.<br />
   The .tree file should be structured as the following...<br />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Parent_Node&nbsp;&nbsp;&nbsp;double&nbsp;&nbsp;&nbsp;double<br />
  Where the index of the line is the child node.<br />
  The .cluster file should be structured as the following...<br />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;NodeID - Node_Name - Size:Related UMLS Terms<br />
 2. Open Cytoscape, must be open for graph to be created.<br />
 3. Run the program and follow requests as given.
