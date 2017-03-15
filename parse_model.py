# TODO: add user-defined functions
import json
import os
from distributions import *
from functions import *

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
# adding a new data type, should not only add it here, but also add it in the preprocess func
data_type = ['cov_matrix', 'simplex','real', 'int', 'vector', 'row_vector', 'matrix']
dependencies = set(['indexing', 'read', 'basic', 'complex', 'discrete', 'continuous'])
user_defined_functions = {}

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
    
  graph = {}
  attr = {}
  var_type = {}
  
  
  for_flag = 0  # the for loops without {}
  if_flag = 0   # the if without {}
  
  state = ''
  bracket_stack = []
  for_stack_map = []
  if_stack = []
  if_stack_buffer = []
  
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
      or '{' in newline \
      or '}' in newline \
      or '=' in newline \
      or '~' in newline:
        lines.append(line)
  
      else:
        lines[-1] = lines[-1].strip('\n') + ' ' + line.strip(' ')
  
    return lines


  def add_to_graph(node, parents, att, var_ty, dependency, debug = ''):
    if not node in graph:
      graph[node] = []
      attr[node] = att
      var_type[node] = var_ty
      if graph_print == 1:
        print 'graph ', debug, node
    if not dependency in dependencies:
      return
    flag = 0
    for p,d in graph[node]:
      if p == set(parents) and d == dependency:
        flag = 1
        break
    if flag == 0:
      graph[node].append((set(parents), dependency))
    if graph_print == 1:
        print 'graph ', debug, node, parents

  # find distribution or function names, return type
  def find_keywords(line): 
    t = ''
    for w in line:
      # if a ~ normal(b+1), return distribution instead of basic computation
      if '~' in line and w in distributions:
        t = distribution_type[distributions[w]]
        if graph_print == 1:
          print 'find type', w, t 
        break
      if w in functions:
        t = function_type[functions[w]]
        if graph_print == 1:
          print 'find type', w, t
        break
      if w in user_defined_functions:
        t = user_defined_functions[w]
        if graph_print == 1:
          print 'find type', w, t
        break
    return t

  op_signs = ['%', '^', ':', ',', '.*', './', '+=', '-=', '/=', '*=', '+', '-', '/', '*', '<=', '<', '>=', ">", '==', '!=', '!', '&&', '||', '\\']
  def replace_op_signs(s):
    for i in op_signs:
      s = s.replace(i,' ')
    return s
  
  lines = preprocess(model)
  #for line in lines:
  #  print line

  for line in lines:
    # ignore whatever can appear within []
    newline = " ".join(line.strip('\n').strip(' ').replace(';', ' '). \
    replace(", ", ","). \
  #  replace(' += ','+=').replace(' -= ','-=').replace(' *= ','*=').replace(' /= ','/='). \
    replace(' + ','+').replace(' - ', '-').replace(' / ', '/').replace(' * ','*'). \
    replace(" < ", "<").replace(' <= ','<=').replace(' > ', '>').replace(' >= ', '>='). \
    replace(" == ", "==").replace(' != ','!=').replace(' !', '!'). \
    replace(" && ", "&&").replace(' || ','||'). \
    replace(' .* ','.*').replace(' ./ ','./'). \
    replace('<-', ' ').\
    replace(' % ', '%'). \
    replace(' \\ ', '\\'). \
    replace('(', ' '). \
    replace(')', ' '). \
    replace('\'',' '). \
    replace('<',' ').replace('>', ' ').split()).split(' ')
  
    if 'transformed' == newline[0] and 'parameters' == newline[1] and '{' in newline:
      bracket_stack.append('transformed parameters')
      state = 'tranformed parameters'
      continue
    elif 'transformed' == newline[0] and 'data' == newline[1] and '{' in newline:
      bracket_stack.append('transformed data')
      state = 'tranformed data'
      continue
    elif 'data' == newline[0] and '{' in newline:
      bracket_stack.append('data')
      state = 'data'
      continue
    elif 'parameters' == newline[0] and '{' in newline:
      bracket_stack.append('parameters')
      state = 'parameters'
      continue
    elif 'model' == newline[0] and '{' in newline:
      bracket_stack.append('model')
      state = 'model'
      continue
    elif 'generated' == newline[0] and 'quantities' == newline[1] and '{' in newline:
      bracket_stack.append('generated quantities')
      state = 'generated quantities'
      continue
    elif 'functions' == newline[0]:
      state = 'functions'
      continue

    if state == "functions":
      # collecting function names
      # find a function declaration
      print newline
      if newline[0] in data_type and '{' in newline:
        user_defined_functions[newline[1]] = 'complex'
      continue
  
    if line_print == 1:
      print newline

    # pop stack first
    if '}' in newline: 
      if if_print == 1 or for_print == 1:
        print 'stack', bracket_stack
      pop = bracket_stack[-1]
      del bracket_stack[-1]
      if pop <> 'for':
        state = ''
      if pop == 'for':
        if for_print == 1:
          print 'for 2 pop', for_stack_map[-1]
        del for_stack_map[-1]
      if pop == 'if' or pop == 'else if' or pop == 'else':
        if if_print == 1:
          print pop, '1 pop', if_stack, bracket_stack, if_flag
        if_stack_buffer = if_stack[-1][:]
        del if_stack[-1]
    # delete }
    if newline[0] == '}' and len(newline) == 1:
      continue
    newlinecat = ''
    for i in newline:
      newlinecat += i + ' '
    newlinecat = newlinecat.strip(' ')
    newline = newlinecat.replace('}',' ').split(' ')    

    if 'for' in newline:
      # now delete the ops that can appear in [], assume for statement does not have []
      # assume one mapping in one for statement only
      # include , + - * / :
      newlinecat = ''
      for i in newline:
        newlinecat += i + ' '
      newlinecat = newlinecat.strip(' ')
      newline = replace_op_signs(newlinecat).replace(']',' ').replace('[', ' ').split(' ')
      bracket_stack.append('for')
      if for_print == 1:
        print 'for loop:', newline

      # start to build for variable map
      flag = 0
      
      # if the loop variable is mapped to real variable
      for k,v in graph.iteritems():
        if k in newline:
            # mapp temp var to real var
            for_stack_map.append((newline[1], k))
            flag = 1
            if for_print == 1:
              print 'for 1 push', for_stack_map[-1]
      # if the loop variable is mapped to outer loop variable
      if flag == 0:
        to_add = []
        for k,v in for_stack_map:
          if k in newline:
            to_add.append((newline[1], v))
            flag = 1
            if for_print == 1:
              print 'for 2 push', to_add[-1]
        for i in to_add:  
          for_stack_map.append(i)
      # if the loop variable is mapped to numbers
      if flag == 0:
        if not newline[-2].isdigit():
          print 'ATTENTION this for loop mapping is strange!'
        for_stack_map.append((newline[1], newline[-2]))
        flag = 1
        if for_print == 1:
          print 'for 3 push', for_stack_map[-1]
      if not '{' in newline:
        for_flag = 1
      continue
    elif 'if' in newline:  # if and else if fall into here  
      # ignore [] in if statement for now
      # assume if and else are in {}
      # there can appear multiple variables in one if statement, push them all together
      # deals with nested if 
      if not '{' in newline:
        if_flag = 1
        print "ATTENTION: If does not have {}!"
      if 'else' in newline:
        bracket_stack.append('else if')
        if_stack.append(if_stack_buffer)
      else:
        bracket_stack.append('if')
      newlinecat = ''
      for i in newline:
        newlinecat += i + ' '
      newlinecat = newlinecat.strip(' ')
      newline = replace_op_signs(newlinecat).replace('[', ' ').replace(']',' ').split(' ')
      to_push = []
      for k,v in graph.iteritems():
        if k in newline:
          to_push.append(k)
      if_stack.append(to_push)
      if if_print == 1:
        print 'if push', to_push, if_stack, bracket_stack
      continue
    elif 'else' in newline: # only else
      bracket_stack.append('else')
      if_stack.append(if_stack_buffer)
      if if_print == 1:
        print 'else push', to_push, if_stack, bracket_stack
      if not '{' in newline:
        if_flag = 1
        print "ATTENTION: else does not have {}!"
      continue
    # {} which does not belong to for or if
    elif '{' in newline:
      bracket_stack.append('empty')
      continue
    else:  
      # find index in the []
      to_process = []
      for i in range(len(newline)):
        if '[' in newline[i]:
          to_process.append(i)
      # declaration with [], [] and var are not connected
      # example: vector[T - 1] b, matrix[N, M] c
      if len(to_process) == 1 and newline[0] in data_type and '[' in newline[to_process[0]][0] == '[' and newline[to_process[0]][-1] == ']':
        name = newline[-1]
        # delete ops that can appear within []: +-*/:!,
        var = replace_op_signs(newline[to_process[0]][1:-1]).split(' ')
        parents = []
        for v in var:
          if v in graph:
            parents.append(v)
        add_to_graph(name, parents, state, newline[0], 'indexing', '1')
        to_process = []
      
      
      if bracket_print == 1:
        print newline, to_process
      # bf[af]
      # or a[b[c]], a[b[c],d[e]], etc
      # vector[N] a[M]
      for i in to_process:
        curr_statement = newline[i]
        while ']' in curr_statement:
        
          if bracket_print == 1:
            print curr_statement
          # find the first ]
          index_a = curr_statement.index(']')
          # find the [ before the first ]
          for j in range(index_a-1, -1, -1):
            if curr_statement[j] == '[':
              index_b = j
              break
          # find the [ before this [
          index_c = 0
          for j in range(index_b-1, -1, -1):
            if curr_statement[j] == '[' or curr_statement[j] in op_signs:
              index_c = j + 1
              break
          # find the content bewteen []
          # delete ops that can appear within []: +-*/:,
          in_bracket = replace_op_signs(curr_statement[index_b + 1: index_a]).split(' ')
          # find the var before this []
          bf_bracket = curr_statement[index_c: index_b]
          if bracket_print == 1:
            print in_bracket, bf_bracket, index_c, index_b, index_a
  
          for a in in_bracket:
            if bracket_print == 1:
              print 'current in []:', a
            # in a for loop and the index is an index of the loop
            mapped_var = []
            if len(for_stack_map) > 0:
              if bracket_print == 1:
                print for_stack_map
              for tmp in for_stack_map:
                if tmp[0] == a:
                  mapped_var.append(tmp[1])
            # not in a for loop or the index does not belong to the loop
            if mapped_var == [] and  a in graph or a.isdigit() and len(in_bracket) == 1:
              mapped_var = [a]
            if mapped_var == []:
              continue
            
            # vector[N] a[M]
            if bf_bracket in data_type and '[' in newline[-1]:
              add_to_graph(newline[-1].split('[')[0], [a], state, bf_bracket, 'indexing', '2')
            # vector[nyears - 1] year_squared;
            elif bf_bracket in data_type:
              add_to_graph(newline[-1], [a], state, bf_bracket, 'indexing', '2')
  
            if not bf_bracket in graph and newline[0] in data_type:
              add_to_graph(bf_bracket, [], state, newline[0], '', '3')
            if bf_bracket in graph:
              for tmp in mapped_var:
                add_to_graph(bf_bracket, [tmp], '', '', 'indexing', '4')

          # delete the [] and contents between them
          new_str = curr_statement[0:index_b] + curr_statement[index_a+1:]
          curr_statement = new_str
        newline[i] = curr_statement 
      # now can safely delete the ops that can appear in []
      # include , + - * /
      find_basic = ''
      newlinecat = ''
      for i in newline:
        newlinecat += i + ' '
      newlinecat = newlinecat.strip(' ')
      if '=' in newlinecat:
          find_basic = 'read'
      for i in ['%', '.*', './', '+', '-', '/', '*', '&&', '||', '\\', '+=', '-=', '*=', '/=']:
        if i in newlinecat:
          find_basic = 'basic'
          break
      newline = replace_op_signs(newlinecat).split(' ')
      # var outside of []
      # declaration with computation, e.g. int a = b - 1;
      if newline[0] in data_type and '=' in newline:
          name = newline[1]
          parents = []
          for k,v in graph.iteritems():
            if k in newline and k <> name:
              parents.append(k)
          t = find_keywords(newline)
          if t == "":
            t = find_basic
          add_to_graph(name, parents, state, newline[0], t, '5')
      # declaration, e.g. int a;
      elif newline[0] in data_type and not newline[-1] in graph: 
          name = newline[-1]
          # if within loop(s), this var is dependent on the loop indices
          parents = []
          if len(for_stack_map) > 0:
            for i in for_stack_map:
              parents.append(i[1]) 
          t = find_keywords(newline)
          if t == "":
            t = find_basic
          add_to_graph(name, parents, state, newline[0], t, '6')
      # computation, e.g. a = b - 1
      elif not newline[0] in data_type:                  
          name = newline[0]
          # if the dest variable is not declared
          t = find_keywords(newline)
          if t == "":
            t = find_basic
          #if not name in graph:
          #  add_to_graph(name, [], 'not declared', 'not declared', t, '7')
          parents = []
          for k,v in graph.iteritems():
            if k in newline and k <> name:
              parents.append(k)
          add_to_graph(name, parents, 'not declared', 'not declared', t, '8')
      if len(if_stack) > 0:
        parents = []
        for i in if_stack:
          for j in i:
            parents.append(j)
        add_to_graph(name, parents, '', '', 'basic', '9')
            
    # flags: here already processed one statement after for or if
    if for_flag == 1 or if_flag == 1: 
      #print 'stack', bracket_stack
      pop = bracket_stack[-1]
      del bracket_stack[-1]
      if pop <> 'for':
        state = ''
      if pop == 'for':
        for_flag = 0
        if for_print == 1:
          print 'for 3 pop', for_stack_map[-1]
        del for_stack_map[-1]
      if pop == 'if' or pop == 'else if':
        if_stack_buffer = if_stack[-1][:]
      if pop == 'if' or pop == 'else if' or pop == 'else':
        if_flag = 0 
        if if_print == 1:
          print pop, '3 pop', if_stack, bracket_stack, if_flag      
        del if_stack[-1]
      
  # postprocess
  # aggeragate integers with largest integer
  for k,v in graph.iteritems():
    flag = 0
    flag1 = 0
    integers = []
    to_delete = []
    for j in range(len(v)):
      (p, dep) = v[j]
      if not dep == 'indexing':
        continue
      # TODO: deal with sth like a[0,0] or a[1,2]
      for i in p:
        if i.isdigit():
          flag = 1
          integers.append(int(i))
          to_delete.append(j)
          break
      for i in p:
        if not i.isdigit() and var_type[i] == "int":
           flag1 = 1
    if flag == 1:
      for i in reversed(to_delete):
        del graph[k][i]
    if len(integers) > 0 and max(integers) > 1 and flag1 == 0:
      graph[k].append((set([max(integers)]), "indexing"))
  
  print '\nGRAPH:'
  for k,v in graph.iteritems():
    parents = []
    for p, dep in v:
      parents.append((list(p), dep))
    graph[k] = parents
    print k, attr[k], var_type[k], graph[k]
  print len(graph), len(attr), len(var_type)
  print '\nUSER_DEFINED_FUNCTIONS:'
  print user_defined_functions

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

  model.close()

if check == 1:
  print '\n\nCheck results:'
  for i in check_results:
    print i[0],'\t', i[1]
  print 'Number of not passed file: ', not_passed, 'out of', len(check_results), 'files, ', not_passed*1.0/len(check_results) 
print 'Total file:', len(files)
print 'Skipped files:', len(skipped_files)
for i in skipped_files:
  print i
