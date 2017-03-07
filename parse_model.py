# caveat: variables are dependent on the index variables 
# real beta[3]; there are 3 betas here, create integers as "variables"
# ignore the arithmetic operations within []
# examples: eps[2:nyear] = eps2[1:nyear - 1], or N_est[t + 1] = N_est[t] * lambda[t];
# a[b[i],c[i]], generate i->b, i->c, b->a, c->a (ignore i->a)
# verified 14 models out of 69 models in BPA
# does not work for one statement with {} in one line

# TODO: if statement, /Users/emma/Projects/Bayesian/profiling/stan_BPA/code/Ch.06/M0.stan

import json
import os

# debugging flags
graph_print = 1
for_print = 0
if_print = 0
line_print = 1

write = 1
check = 1
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
files = ['/Users/emma/Projects/Bayesian/profiling/stan_BPA/code/Ch.04/GLMM5.stan']
output = '/Users/emma/Projects/Bayesian/profiling/stan_BPA/outputs/probgraph'
data_type = ['real', 'int', 'vector', 'row_vector', 'matrix']

for modelfile in files:

  print modelfile
  model = open(modelfile,'r')
  
  if check == 1:
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
  iter_index = {}
  if_stack = []
  if_stack_buffer = []
  
  # deal with one statement in multiple lines
  # ignore comments
  def preprocess(model):
    # if a line does not have key words, = or ~, combine it with previous line
    lines = []
    for line in model:
      line = line.strip('\n').strip(' ')
      if line == '':
        continue
      if line.strip(' ')[0] == '/' and line.strip(' ')[1] == '/':
        continue
      if '//' in line:
        line = line.split('//')[0].strip(' ')  
  
      newline = " ".join(line.strip('\n').strip(' ').replace(';', ' '). \
      replace(",", " ").replace(":", " "). \
      replace("[", " ").replace("]", " "). \
      replace('+',' '). \
      replace('.*',' '). \
      replace('<-', ' ').\
      replace('-', ' '). \
      replace('/', ' '). \
      replace('*',' '). \
      replace('^',' '). \
      replace('(', ' '). \
      replace(')', ' '). \
      replace('\'',' '). \
      replace('<',' ').replace('>', ' ').split()).split(' ')
  
      if 'real' in newline \
      or 'int' in newline \
      or 'vector' in newline \
      or 'row_vector' in newline \
      or 'matrix' in newline \
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
  
  lines = preprocess(model)
  #for line in lines:
  #  print line
  
  for line in lines:
    # ignore whatever can appear within []
    newline = " ".join(line.strip('\n').strip(' ').replace(';', ' '). \
    replace(", ", ","). \
    replace(' + ','+'). \
    replace('.*',' '). \
    replace('<-', ' ').\
    replace(' - ', '-'). \
    replace(' / ', '/'). \
    replace(' * ','*'). \
    replace('(', ' '). \
    replace(')', ' '). \
    replace('~', ' ').\
    replace('\'',' '). \
    replace('<',' ').replace('>', ' ').split()).split(' ')
    #newline = " ".join(newline.replace('/',' ').split()).split(' ')
    
  
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
  
    if line_print == 1:
      print newline

    # pop stack first
    if '}' in newline: 
      print 'stack', bracket_stack
      pop = bracket_stack[-1]
      del bracket_stack[-1]
      if pop <> 'for':
        state = ''
      if pop == 'for':
        if for_print == 1:
          print 'for 2 pop', for_stack_map[-1]
        iter_index.pop(for_stack_map[-1][0], None)
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
      newline = newlinecat.replace('^',' ').replace(',',' ').replace(':',' ').replace('+',' ').replace('-',' ').replace('*',' ').replace('/',' ').replace('[', ' ').replace(']',' ').split(' ')
      bracket_stack.append('for')
      for k,v in graph.iteritems():
        if k in newline:
            for_stack_map.append((newline[1], k))
            iter_index[newline[1]] = len(for_stack_map)-1
            if for_print == 1:
              print 'for 1 push', for_stack_map[-1]
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
      newline = newlinecat.replace(',',' ').replace('^',' ').replace(':',' ').replace('+',' ').replace('-',' ').replace('*',' ').replace('/',' ').replace('[', ' ').replace(']',' ').split(' ')
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
    else:  
      # find index in the []
      to_process = []
      for i in range(len(newline)):
        if '[' in newline[i]:
          to_process.append(i)
      # declaration with [], [] and var are not connected
      # example: vector<lower=0>[nconds] gplus, or vector<lower=0>[T - 1] lambda
      if len(to_process) == 1 and newline[0] in data_type and '[' in newline[to_process[0]][0] == '[' and newline[to_process[0]][-1] == ']':
        name = newline[-1]
        # delete ops that can appear within []: +-*/:,
        var = newline[to_process[0]][1:-1].replace(',',' ').replace('^',' ').replace(':',' ').replace('+',' ').replace('-',' ').replace('*',' ').replace('/',' ').split(' ')
        graph[name] = set()
        if graph_print == 1:
          print 'graph 0', name
        for v in var:
          if v in graph:
            graph[name].add(v)
            if graph_print == 1:
              print 'graph 1', name, v
        attr[name] = state
        var_type[name] = newline[0]
        to_process = []
      
      print newline, to_process
      # bf[af]
      # or a[b[c]], a[b[c],d[e]], etc
      for i in to_process:
        curr_statement = newline[i]
        while ']' in curr_statement:
        
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
            if curr_statement[j] == '[' or curr_statement[j] == ',':
              index_c = j + 1
              break
          # find the content bewteen []
          # delete ops that can appear within []: +-*/:,
          in_bracket = curr_statement[index_b + 1: index_a].replace(':',' ').replace(',', ' ').replace('^',' ').replace('/',' ').replace('+',' ').replace('-',' ').replace('*',' ').split(' ')
          # find the var before this []
          bf_bracket = curr_statement[index_c: index_b]
          #print in_bracket, bf_bracket, index_c, index_b, index_a
  
          for a in in_bracket:
            # in a for loop and the index is an index of the loop
            if len(for_stack_map) > 0 and a in iter_index and iter_index[a] < len(for_stack_map):
              mapped_var = for_stack_map[iter_index[a]][1]
            # not in a for loop or the index does not belong to the loop
            elif a in graph or a.isdigit() and len(in_bracket) == 1:
              mapped_var = a
            else:
              continue
            # deal with sth like this: vector[nyears] year_squared;
            # and vector[T - 1] lambda
            if bf_bracket in data_type:
              graph[newline[-1]] = set([a])
              attr[newline[-1]] = state
              var_type[newline[-1]] = bf_bracket
              if graph_print == 1:
                print 'graph 2',newline[-1], a, graph[newline[-1]]
  
            if not bf_bracket in graph and newline[0] in data_type:
              graph[bf_bracket] = set()
              if graph_print == 1:
                print 'graph 3', bf_bracket
              attr[bf_bracket] = state
              var_type[bf_bracket] = newline[0]
            if bf_bracket in graph:
              graph[bf_bracket].add(mapped_var)
              if graph_print == 1:
                print 'graph 4', bf_bracket, mapped_var
          # delete the [] and contents between them
          new_str = curr_statement[0:index_b] + curr_statement[index_a+1:]
          curr_statement = new_str
        newline[i] = curr_statement 
      # now can safely delete the ops that can appear in []
      # include , + - * /
      newlinecat = ''
      for i in newline:
        newlinecat += i + ' '
      newlinecat = newlinecat.strip(' ')
      newline = newlinecat.replace(',',' ').replace('^',' ').replace('+',' ').replace('-',' ').replace('*',' ').replace('/',' ').split(' ')
      # var outside of []
      if newline[0] in data_type and not newline[-1] in graph: # declaration
          name = newline[-1]
          graph[name] = set()
          if graph_print == 1:
            print 'graph 5', name
          attr[name] = state
          var_type[name] = newline[0]
          # if within loop(s), this var is dependent on the loop indices
          if len(for_stack_map) > 0:
            for i in for_stack_map:
              graph[name].add(i[1]) 
              if graph_print == 1:
                print 'graph 6', name, i[1]
      elif not newline[0] in data_type:                   # computation
          name = newline[0]
          if not name in graph: # if the dest variable is not declared
            graph[name] = set()
            attr[name] = 'not declared'
            var_type[name] = 'not declared'
            if graph_print == 1:
              print 'graph', name, 'not declared'
          for k,v in graph.iteritems():
            if k in newline and k <> name:
              graph[name].add(k)
              if graph_print == 1:
                print 'graph 7', name, k
      if len(if_stack) > 0:
        for i in if_stack:
          for j in i:
            graph[name].add(j)
            
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
        iter_index.pop(for_stack_map[-1][0], None)
        del for_stack_map[-1]
      if pop == 'if' or pop == 'else if':
        if_stack_buffer = if_stack[-1][:]
      if pop == 'if' or pop == 'else if' or pop == 'else':
        if_flag = 0 
        if if_print == 1:
          print pop, '3 pop', if_stack, bracket_stack, if_flag      
        del if_stack[-1]
      
      
      
  # postprocess
  # aggeragate integers with integer variable dependencies
  for k,v in graph.iteritems():
    flag1 = 0
    flag2 = 0
    for i in v:
      if i in graph and var_type[i] == 'int':
        flag2 = 1
    if flag2 == 1:
      to_delete = []
      for i in v:
        if i.isdigit():
          to_delete.append(i)
      for i in to_delete:
          graph[k].remove(i)
  
  print 'GRAPH:'
  for k,v in graph.iteritems():
    print k, attr[k], var_type[k], v
    graph[k] = list(v)
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
      if graph[k] <> chk_graph[k]:
        flag = 0
        print 'Graph is wrong: ',k, graph[k], chk_graph[k]
    if flag == 0:
      print 'Does not pass correction check.'
    else:
      print 'Correstion Check Passed.'

  model.close()
