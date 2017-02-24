
# one statement has to be in one line

model = open('/Users/emma/Projects/Bayesian/profiling/stan_BPA/code/Ch.03/GLM_Binomial.stan','r')
graph = {}
attr = {}
data_type = ['real', 'int', 'vector', 'row_vector', 'matrix']
var_type = {}

graph_print = 1
for_print = 0

for_flag = 0 # the for loops without {}

state = ''
bracket_stack = []
for_stack_map = []
iter_index = {}
for line in model:
  newline = " ".join(line.strip('\n').strip(' ').replace(';', ' '). \
  #replace('/',' '). \
  replace('+',' '). \
  replace('<-', ' ').replace('-', ' ').replace('*',' '). \
  replace('(', ' ').replace(')', ' '). \
  #replace(']', ' ').replace('[',' '). \
  replace('~', ' ').\
  #replace(',',' '). \
  replace(':',' '). \
  replace('<',' ').replace('>', ' ').split())

  if newline == '':
    continue
  if newline[0] == '/' and newline[1] == '/':
    continue
  if '//' in newline:
    newline = newline.split('//')[0].strip(' ')
  
  newlinecat = " ".join(newline.replace('/',' ').split())
  newline = " ".join(newline.replace('/',' ').split()).split(' ')
  

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

  print newline
  if 'logit_p' in graph:
    print graph['logit_p']
  if 'for' in newline:
    bracket_stack.append('for')
    newline = " ".join(newlinecat.replace('[', ' ').replace(']',' ').split()).split(' ')
    for k,v in graph.iteritems():
      if k in newline:
          for_stack_map.append((newline[1], k))
          iter_index[newline[1]] = len(for_stack_map)-1
          if for_print == 1:
            print 'for 1 push', for_stack_map[-1]
    if not '{' in newline:
      for_flag = 1
    continue
  else:  
    # find index in the []
    to_process = []
    for i in newline:
      if '[' in i:
        to_process.append(i)
    # declaration with [], [] and var are not connected
    # example: vector<lower=0>[nconds] gplus;
    if len(to_process) == 1 and newline[0] in data_type and to_process[0][0] == '[' and to_process[0][-1] == ']':
      name = newline[-1]
      graph[name] = set(to_process[0][1:-1])
      if graph_print == 1:
        print 'graph 1', name, to_process[0][1:-1]
      attr[name] = state
      var_type[name] = newline[0]
      to_process = []
    
    # bf[af]
    for i in to_process:
      bf = i.split('[')[0] # outside of []
      af = [tmp.strip(' ') for tmp in i.split('[')[-1].strip(']').split(',')] # inside of []
      for a in af:
        # in a for loop and the index is an index of the loop
        if len(for_stack_map) > 0 and a in iter_index and iter_index[a] < len(for_stack_map):
          mapped_var = for_stack_map[iter_index[a]][1]
        # not in a for loop or the index does not belong to the loop
        elif a in graph:
          mapped_var = a
        else:
          continue
        # deal with sth like this: vector[nyears] year_squared;
        if bf in data_type:
          graph[newline[-1]] = set(a)
          attr[newline[-1]] = state
          var_type[newline[-1]] = bf
          if graph_print == 1:
            print 'graph 2',newline[-1], a

        if not bf in graph and newline[0] in data_type:
          graph[bf] = set()
          if graph_print == 1:
            print 'graph 3', bf
          attr[bf] = state
          var_type[bf] = newline[0]
        if bf in graph:
          graph[bf].add(mapped_var)
          if graph_print == 1:
            print 'graph 4', bf, mapped_var
    # now delete the [] and contents between them
    for i in range(len(newline)):
      if '[' in newline[i]:
        newline[i] = newline[i].split('[')[0]
    # now can safely delete ,
    for i in range(len(newline)):
      if ',' in newline[i]:
        newline[i] = newline[i].replace(',','')
      
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
    elif not newline[0] in data_type: #TODO condition is wrong                      # computation
        name = newline[0]
        for k,v in graph.iteritems():
          if k in newline and k <> name:
            graph[name].add(k)
            if graph_print == 1:
              print 'graph 7', name, k
    
  if '}' in newline or for_flag == 1:
    print 'stack', bracket_stack
    for_flag = 0
    pop = bracket_stack[-1]
    del bracket_stack[-1]
    if pop <> 'for':
      state = ''
    if pop == 'for':
      if for_print == 1:
        print 'for 2 pop', for_stack_map[-1]
      iter_index.pop(for_stack_map[-1][0], None)
      del for_stack_map[-1]
    

print 'GRAPH:'
for k,v in graph.iteritems():
  print k, attr[k], var_type[k], v
print len(graph), len(attr), len(var_type)
