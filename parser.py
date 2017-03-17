from distributions import *
from functions import *
# adding a new data type, should not only add it here, but also add it in the preprocess func
data_type = ['cov_matrix', 'simplex','real', 'int', 'vector', 'row_vector', 'matrix']
dependencies = set(['indexing', 'read', 'basic', 'complex', 'discrete', 'continuous'])
op_signs = ['%', '^', ':', ',', '.*', './', '+=', '-=', '/=', '*=', '+', '-', '/', '*', '<=', '<', '>=', ">", '==', '!=', '!', '&&', '||', '\\']

def parser(lines, line_print, graph_print, for_print, if_print, bracket_print):

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

  user_defined_functions = {}

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

  def replace_op_signs(s):
    for i in op_signs:
      s = s.replace(i,' ')
    return s
  

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
        print graph

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
          if len(for_stack_map) > 0:
            for i in for_stack_map:
              add_to_graph(name, [i[1]], state, newline[0], 'indexing', '6')
      # declaration, e.g. int a;
      elif newline[0] in data_type and not newline[-1] in graph: 
          name = newline[-1]
          # if within loop(s), this var is dependent on the loop indices
          add_to_graph(name, [], state, newline[0], '', '7')
          if len(for_stack_map) > 0:
            for i in for_stack_map:
              add_to_graph(name, [i[1]], state, newline[0], 'indexing', '8')
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
          add_to_graph(name, parents, 'not declared', 'not declared', t, '9')
      if len(if_stack) > 0:
        parents = []
        for i in if_stack:
          for j in i:
            parents.append(j)
        add_to_graph(name, parents, '', '', 'basic', '10')
            
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

  print '\nuser defined functions:'
  print user_defined_functions
  return graph, attr, var_type
