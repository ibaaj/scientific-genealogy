from graphviz import Digraph
import json


### ADD THE ID of your first ancestor:
# e.g. Euler https://www.mathgenealogy.org/id.php?id=38586
# is : 38586
# and your name
IDANCESTOR =  38586
YOURNAME = "YOUR NAME"

dot = Digraph()



with open('authors.json') as json_file:
    authors = json.load(json_file)
    print(authors)

with open('edges.txt') as json_file:
    edges = json.load(json_file)
    print(edges)


for auth in authors:
    dot.node(auth, authors[auth])

dot.node(str(1), YOURNAME)


for edge in edges:
    dot.edge(edge[1],edge[0])

dot.edge(str(1),IDANCESTOR)

print(dot.source)
dot.render(view=True)

