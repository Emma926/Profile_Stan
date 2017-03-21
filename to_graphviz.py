# Take the output and paste in http://www.webgraphviz.com
import json
import sys

graphfile = sys.argv[1]

with open(graphfile) as fin:
   [graph, attr, var_type] = json.load(fin)

param_node = []
data_node = []
number_node = []
edges = []
depends = []
for node, v in graph.iteritems():
  if 'data' in attr[node] and len(v) == 0:
    number_node.append(node)
  elif 'data' in attr[node]:
    data_node.append(node)
  else:
    param_node.append(node)

  for parent, depend in v:
    for p in parent:
        edges.append(p + '->' + node)
        depends.append(depend)

s = 'Digraph variables {\nnode [shape=circle,fixedsize=true,width=0.9];'
for i in param_node:
  s += ' ' + i + ';'
s += '\nnode [shape=box];'
for i in data_node:
  s += ' ' + i + ';'
s += '\nnode [shape=diamond,style=filled,color=lightgrey];'
for i in number_node:
  s += ' ' + i + ';'
s += '\n'
for e in edges:
  s += e + ';\n'
s += 'overlap=false\n\
label="graphical model dependency"\n\
fontsize=12;\n}'

print s
