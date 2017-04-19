import copy

def generate_data_list(data_file_name):
  data_list = {}
  f = open(data_file_name, 'r')
  read_data = 0
  start_bracket = 0
  for line in f:
    if '\"' in line:
      line = line.replace('\"','')
    elif '\'' in line:
      line = line.replace('\'','')
    line = line.strip('\n').strip(' ')

    if '<-' in line and not '=' in line:
      linesplit = [i.strip(' ') for i in line.split('<-')]
      read_var = 1
      read_data = 0
    elif not '<-' in line and '=' in line:
      linesplit = [i.strip(' ') for i in line.split('=')]
      read_var = 1
      read_data = 0

    if read_data == 1:
      if 'c' in line and '(' in line:
        linesplit = [i.strip(' ') for i in line.split('(')[-1].split(',')]
        start_bracket = 1
      elif ')' in line:
        linesplit = [i.strip(' ') for i in line.split(')')[0].split(',')]
      else:
        linesplit = [i.strip(' ') for i in line.split(',')]
      for i in linesplit:
        if i <> '':
          all_data.append(float(i))
      if ')' in line or start_bracket == 0:
        read_data = 0
        data_list[var_name] = all_data
        start_bracket = 0
      continue

    if read_var == 1:
      if linesplit[-1].isdigit():
        data_list[linesplit[0]] = [int(linesplit[-1])]
      elif not linesplit[-1].isdigit():
        var_name = linesplit[0]
        read_data = 1
        all_data = []
  f.close()
  return data_list
  
def generate_dynamic_graph(data_list, graph, attr, var_type):
  dy_graph = {}
  dy_attr = {}
  dy_var_type = {}
  expanded = set()
  expand_map = {} # variable: index var / int

  for k,v in graph.iteritems():
    if len(v) == 0 and not k.isdigit() and not k in data_list:
      dy_graph[k] = []
      dy_attr[k] = attr[k]
      dy_var_type[k] = var_type[k]
      
    for parents, dep in v:
      if len(parents) == 0:
        dy_graph[k] = graph[k]
        dy_attr[k] = attr[k]
        dy_var_type[k] = var_type[k]
        break
      for p in parents:
        if p in data_list and dep == 'indexing':
          for i in range(data_list[p]):
            dy_graph[k + '.' + str(i)] = []
            dy_attr[k + '.' + str(i)] = attr[k]
            dy_var_type[k + '.' + str(i)] = var_type[k]
          expanded.add(k)
          expand_map[k] = p
        elif p.isdigit() and dep == 'indexing':
          for i in range(int(p)):
            dy_graph[k + '.' + str(i)] = []
            dy_attr[k + '.' + str(i)] = attr[k]
            dy_var_type[k + '.' + str(i)] = var_type[k]
          expanded.add(k)
          expand_map[k] = p

  print '--------------------------------------'
  to_print = []
  for k,v in dy_graph.iteritems():
    to_print.append(k)
  print sorted(to_print)
  print '--------------------------------------'

  for k,v in graph.iteritems():
    for parents, dep in v:
      homo_expand = []
      hete_expand = []
      rest = []

      if len(parents) == 0:
        break
  
      for p in parents: 
        if (p in data_list or p.isdigit()) and dep == 'indexing':
          continue
        if p in expanded and k in expanded and expand_map[p] == expand_map[k]:
          homo_expand.append(p)
        elif p in expanded and k in expanded and expand_map[p] <> expand_map[k]:
          hete_expand.append(p)
        elif not p in expanded and k in expanded:
          rest.append(p)
        else:
          print 'Attention 1', k, p

      if len(homo_expand) == 0 and len(hete_expand) == 0 and len(rest) == 0:
        continue

      new_parents = set()
      for i in hete_expand:
        if expand_map[i].isdigit():
          n = int(expand_map[i])
        elif expand_map[i] in data_list:
          n = data_list[expand_map[i]]
        else:
          print 'Attention 2', i, expand_map[i]
        for j in range(n):
          new_parents.add(i + '.' + str(j))
      for i in rest:
        new_parents.add(i)

      if expand_map[k].isdigit():
        n = int(expand_map[k])
      elif expand_map[k] in data_list:
        n = data_list[expand_map[k]]
      else:
        print 'Attention 3', k, expand_map[k] 

      for i in range(n):
        curr_parents = copy.deepcopy(new_parents)
        for j in homo_expand:
          curr_parents.add(j + '.' + str(i)) 
        dy_graph[k + '.' + str(i)].append((curr_parents, dep))

  return dy_graph, dy_attr, dy_var_type
         
