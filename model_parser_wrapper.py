import json
import os
import fnmatch
from parser import *
from preprocess import *

# debugging flags
line_print = 1 
graph_print = 1
for_print = 0
if_print = 0
bracket_print = 1

write = 1
check = 0

# has the same name as functions and data types
invalid_models_type1 = []
invalid_graphs_type1 = []
# has op sign in the var name
invalid_models_type2 = []
invalid_graphs_type2 = []
# unconnected variables
invalid_models_type3 = []
invalid_graphs_type3 = []
# invalid data type
invalid_models_type4 = []
invalid_graphs_type4 = []


root = '../code'
files = []
for root, dirnames, filenames in os.walk(root):
    for filename in fnmatch.filter(filenames, '*.stan'):
        files.append(os.path.join(root, filename))

#for f in files:
#  print f
#print len(files)

output = '../outputs/probgraph'

if check == 1:
  check_results = []
  not_passed = 0

for modelfile in files:

  print modelfile
  model = open(modelfile,'r')
  
  if check == 1:
    if not os.path.isfile(modelfile.replace('.stan', '.probgraph')):
      continue
    with open(modelfile.replace('.stan', '.probgraph')) as fin:
         [chk_graph, chk_attr, chk_var_type] = json.load(fin)
    
  

  lines = preprocess(model)
  model.close()
  #for line in lines:
  #  print line
  graph, attr, var_type, invalid= parser(lines, line_print, graph_print, for_print, if_print, bracket_print)

  if invalid == 1:
    invalid_models_type1.append(modelfile)
    invalid_graphs_type1.append(os.path.join(output, modelfile.split('/')[-1].replace('.stan', '.probgraph')))
  if invalid == 2:
    invalid_models_type2.append(modelfile)
    invalid_graphs_type2.append(os.path.join(output, modelfile.split('/')[-1].replace('.stan', '.probgraph')))
  if invalid == 3:
    invalid_models_type3.append(modelfile)
    invalid_graphs_type3.append(os.path.join(output, modelfile.split('/')[-1].replace('.stan', '.probgraph')))
  if invalid == 4:
    invalid_models_type4.append(modelfile)
    invalid_graphs_type4.append(os.path.join(output, modelfile.split('/')[-1].replace('.stan', '.probgraph')))
  
  print '\nGRAPH:'
  for k,v in graph.iteritems():
    parents = []
    for p, dep in v:
      parents.append((list(p), dep))
    graph[k] = parents
    print k, attr[k], var_type[k], graph[k]
  print len(graph), len(attr), len(var_type)

  if write == 1:
    with open(os.path.join(output, modelfile.split('/')[-1].replace('.stan', '.probgraph')), 'w') as fout:
      json.dump([graph, attr, var_type], fout)
  
  if check == 1:
    flag = 1
    if len(graph) <> len(chk_graph):
      flag = 0
      print 'Graph length is wrong: ', len(graph), len(chk_graph)
    for k,v in graph.iteritems():
      if len(graph[k])  <> len(chk_graph[k]):
          print "WRONG:\t", k
          print "GIVEN:\t", graph[k]
          print "CORRECT:\t", chk_graph[k]
          flag = 0
          continue
      for p,d in v:
        f = 0
        for a,b in graph[k]:
          if a==p and d==b:
            f = 1
        if f == 0:
          print "WRONG:\t", k
          print "GIVEN:\t", graph[k]
          print "CORRECT:\t", chk_graph[k]
          flag = 0
          break
    if flag == 0:
      check_results.append((modelfile, 'NO'))
      print 'Does not pass correction check.'
      not_passed += 1
    else:
      check_results.append((modelfile, 'YES'))
      print 'Correction Check Passed.'


if check == 1:
  print '\n\nCheck results:'
  for i in check_results:
    print i[0],'\t', i[1]
  print 'Number of not passed file: ', not_passed, 'out of', len(check_results), 'files, ', not_passed*1.0/len(check_results) 
print 'Total file:', len(files)
print '\nInvalid files:', len(invalid_models_type1) + len(invalid_models_type3) + len(invalid_models_type3)
print '1. Invalid file, variables have the same name as data types or functions:'
print invalid_models_type1
print invalid_graphs_type1
print '2. Invalid file, variables have op signs'
print invalid_models_type2
print invalid_graphs_type2
print '3. Invalid file, unconnected variables'
print invalid_models_type3
print invalid_graphs_type3
print '4. Invalid file, invalid data type'
print invalid_models_type4
print invalid_graphs_type4
