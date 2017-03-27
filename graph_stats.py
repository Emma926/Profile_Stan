import os
import json

graph_dirs = [
  '/Users/emma/Projects/Bayesian/profiling/stan_ARM/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_BCM/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_BPA/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_bugs/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_knitr/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_misc/outputs/probgraph'
]
files = []
for d in graph_dirs:
  fs = os.listdir(d)
  for f in fs:
    files.append(os.path.join(d,f))
print "# of Models: ", len(files)

names = []

# summary
nodes = []
edges = []
dependencies = []
layers = []

# types of variables
params = []
dataparams = []

# computations: basic/complex
basic_comp = []
complex_comp = []

# computations: int/real/vector/matrix
level = ['matrix', 'vector', 'real', 'int']
var_type_map = {'not declared': 'real', 'int':'int','real':'real', 'matrix':'matrix', 'cov_matrix':'matrix', 'corr_matrix':'matrix', 'cholesky_factor_cov':'matrix', 'cholesky_factor_corr':'matrix', 'vector':'vector', 'simplex':'vector', 'unit_vector':'vector', 'ordered':'vector', 'positive_ordered':'vector', 'row_vector':'vector'}
computations = {'matrix':[], 'vector':[], 'real':[], 'int':[]}

# distributions
discrete = []
continuous = []

def _dfs(curr_node, graph, visiting):  
  if curr_node in visiting:
    return True
  if not curr_node in graph:
    return False
  visiting.add(curr_node)
  for n in graph[curr_node]:
    if _dfs(n, graph, visiting) == True:
      return True
  visiting.remove(curr_node)
  return False

def dfs(leaves, graph):
  for n in leaves:
    if _dfs(n, graph, set()) == True:
      return True
  return False

def bfs(leaves, graph):
    queue = []
    node_depth = {}
    for i in leaves:
      queue.append((i,1))
      node_depth[i] = 1
    while len(queue) > 0:
      node, l = queue[0]
      del queue[0]
      for parents, dep in graph[node]:
        for p in parents:
          if str(p).isdigit():
            continue
          if p in node_depth:
            d = node_depth[p]
          else:
            d = 0
          queue.append((p, max([d, l+1])))
          node_depth[p] = max([d, l+1])
    max_depth = 0
    for k,v in node_depth.iteritems():
      if v > max_depth:
        max_depth = v
    return max_depth


c = 0
for graphfile in files:
    print c,graphfile
    c += 1
    with open(graphfile) as fin:
         [graph, attr, var_type] = json.load(fin)
    name = graphfile.split('stan_')[-1].split('/')[0] + '-' + graphfile.split('/')[-1].replace('.probgraph', '')
    names.append(name)

    param_c = 0
    data_c = 0
    for k,v in attr.iteritems():
      if 'parameter' in v:
        param_c += 1
      elif 'data' in v:
        data_c += 1

    params.append(param_c)
    dataparams.append(data_c)
    
    edge_c = 0
    depend_c = 0
    basic_c = 0
    complex_c = 0
    dis_c = 0
    con_c = 0
    ty_c = {'matrix':0, 'vector':0, 'real':0, 'int':0}
    leaves = set()
    for node, v in graph.iteritems():
      # initialize the leaves as all nodes
      leaves.add(node)
      for parents, dep in v:
        depend_c += 1
        edge_c += len(parents)
        t = []
        if dep == 'discrete':
          dis_c += 1
          continue
        elif dep == 'continuous':
          con_c += 1
          continue
        if dep == 'read' or dep == 'basic':
          basic_c += 1
        if dep == 'complex':
          complex_c += 1
        for p in parents:
          if str(p).isdigit():
            t.append(1)
            continue
          t.append(level.index(var_type_map[var_type[p]]))
        t.append(level.index(var_type_map[var_type[node]]))
        ty_c[level[min(t)]] += 1
    discrete.append(dis_c)
    continuous.append(con_c)
    for k,v in ty_c.iteritems():
      computations[k].append(v)
    basic_comp.append(basic_c)
    complex_comp.append(complex_c)
    nodes.append(len(graph))
    edges.append(edge_c)
    dependencies.append(depend_c)

    # remove the nodes that have children
    # remain nodes are leaves
    for node, v in graph.iteritems():
      for parents, dep in v:
        for p in parents:
          if p in leaves:
            leaves.remove(p)

    # check whether the graph has loops or not
    # dfs    
    new_graph = {}
    for node,v in graph.iteritems():
      new_graph[node] = set()
      for parents, dep in v:
        for p in parents:
          new_graph[node].add(p)
    iscyclic = dfs(leaves, new_graph)
    print iscyclic
    if iscyclic:
      layers.append(99999)
    
    if not iscyclic:
      # max depth by bfs
      layers.append(bfs(leaves, graph))
          
print 'names = ' + str(names)
print 'nodes = ' + str(nodes)
print 'edges = ' + str(edges)
print 'layers = ' + str(layers)
print 'dependencies = ' + str(dependencies)
print 'params = ' + str(params)
print 'dataparams = ' + str(dataparams)
print 'basic_comp = ' + str(basic_comp)
print 'complex_comp = ' + str(complex_comp)
for k in level:
  print k + '_comp = ' + str(computations[k])
print 'discrete = ' + str(discrete)
print 'continuous = ' + str(continuous)
