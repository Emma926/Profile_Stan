import json
import os
from parser import *

# debugging flags
line_print = 0 
graph_print = 0
for_print = 0
if_print = 0
bracket_print = 0

write = 1
check = 1

skipped_files = []

root = '/Users/emma/Projects/Bayesian/profiling/stan_BPA/code'
paths = []
files = []
# find all the paths
fs = os.listdir(root)
for f in fs:
    if 'Ch' in f:
      paths.append(os.path.join(root, f))
for path in paths:
  fs = os.listdir(path)
  for f in fs:
    if '.stan' in f:
      files.append(os.path.join(path, f))
#for f in files:
#  print f

output = '/Users/emma/Projects/Bayesian/profiling/stan_BPA/outputs/probgraph'

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
    
  def hasfunction(line):
    for i in line:
      if i in functions:
        return True
    return False
  
  # deal with one statement in multiple lines
  # ignore comments
  def preprocess(model):
    # if a line does not have key words, = or ~, combine it with previous line
    lines = []
    ignore = 0
    for line in model:
      line = line.strip('\n').strip(' ')
      if "*/" in line:
        ignore = 0
        continue
      if line == '' or ignore == 1:
        continue
      if line.strip(' ')[0] == '/' and line.strip(' ')[1] == '/':
        continue
      if '//' in line:
        line = line.split('//')[0].strip(' ')  
      if '/*' in line:
        ignore = 1
  
      line = line.replace('<-', "=")
      if '{' in line and not ' {' in line:
        line = line.replace('{', ' {')

      newline = " ".join(line.strip('\n').strip(' ').replace(';', ' '). \
      replace(",", " ").replace(":", " "). \
      replace("[", " ").replace("]", " "). \
      replace('+',' '). \
      replace('.*',' '). \
      replace('<-', ' ').\
      replace('-', ' '). \
      replace('/', ' '). \
      replace('*',' '). \
      replace('!',' '). \
      replace('^',' '). \
      replace('(', ' ( '). \
      replace(')', ' ) '). \
      replace('\'',' '). \
      replace('<',' ').replace('>', ' ').split()).split(' ')
      
      # declaration, delete <> and contents in between
      if newline[0] in data_type and '<' in line and '>' in line:
        ind_a = line.index('<')
        ind_b = line.index('>')
        line = line[0:ind_a] + line[ind_b+1:]

      if ')' in newline and not '(' in newline:
        lines[-1] = lines[-1].strip('\n') + ' ' + line.strip(' ')
      elif 'real' in newline \
      or 'int' in newline \
      or 'vector' in newline \
      or 'row_vector' in newline \
      or 'matrix' in newline \
      or 'cov_matrix' in newline \
      or 'simplex' in newline \
      or 'for' in newline \
      or 'if' in newline \
      or 'else' in newline \
      or '{' in newline \
      or '}' in newline \
      or '=' in newline \
      or '~' in newline \
      or hasfunction(newline) and not (line[0] in op_signs or lines[-1][-1] in op_signs):
        lines.append(line)
  
      else:
        lines[-1] = lines[-1].strip('\n') + ' ' + line.strip(' ')
  
    return lines

  lines = preprocess(model)
  model.close()
  #for line in lines:
  #  print line
  graph, attr, var_type = parser(lines, line_print, graph_print, for_print, if_print, bracket_print)

  
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
print 'Skipped files:', len(skipped_files)
for i in skipped_files:
  print i
