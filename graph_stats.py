import os
import json
import numpy

graph_dirs = [
  '/Users/emma/Projects/Bayesian/profiling/stan_ARM/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_BCM/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_BPA/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_bugs/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_knitr/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_misc/outputs/probgraph',
  '/Users/emma/Projects/Bayesian/profiling/stan_stancon/outputs/probgraph'
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
avg_width = []

# types of variables
params = []
dataparams = []
otherparams = []
indexedparams = [] # parameters whose numbers are governed by int data params

# computations: basic/complex
basic_comp = []
complex_comp = []

indexing = []

# computations: int/real/vector/matrix
level = ['matrix', 'vector', 'real', 'int']
var_type_map = {'not declared': 'real', 'int':'int','real':'real', 'matrix':'matrix', 'cov_matrix':'matrix', 'corr_matrix':'matrix', 'cholesky_factor_cov':'matrix', 'cholesky_factor_corr':'matrix', 'vector':'vector', 'simplex':'vector', 'unit_vector':'vector', 'ordered':'vector', 'positive_ordered':'vector', 'row_vector':'vector'}
computations = {'matrix':[], 'vector':[], 'real':[], 'int':[]}

# distributions
discrete = []
continuous = []

def _dfs(curr_node, graph, leaves, visit):  
  if curr_node in visit:
    return 0
  if curr_node in leaves:
    return 1
  visit.add(curr_node)
  l = []
  for n in graph[curr_node]:
    l.append(_dfs(n, graph, leaves, visit))
  visit.remove(curr_node)
  return 1 + max(l)

def dfs(start, leaves, graph):
  l = []
  for n in start:
    l.append(_dfs(n, graph, leaves, set()))
  return max(l)


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
    other_c = 0
    for k,v in attr.iteritems():
      if 'parameter' in v:
        param_c += 1
      elif 'data' in v:
        data_c += 1
      else:
        other_c += 1

    params.append(param_c)
    dataparams.append(data_c)
    otherparams.append(other_c)
    
    edge_c = 0
    depend_c = 0
    basic_c = 0
    complex_c = 0
    dis_c = 0
    con_c = 0
    indexed_set = set()
    index_c = 0
    
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
        if dep == 'indexing' and parents[0] in var_type and var_type[parents[0]] == 'int':
          indexed_set.add(node)
        if dep == 'indexing':
          index_c += 1
          continue
        for p in parents:
          if str(p).isdigit():
            t.append(1)
            continue
          t.append(level.index(var_type_map[var_type[p]]))
        t.append(level.index(var_type_map[var_type[node]]))
        ty_c[level[min(t)]] += 1
    
    indexedparams.append(len(indexed_set))
    discrete.append(dis_c)
    continuous.append(con_c)
    for k,v in ty_c.iteritems():
      computations[k].append(v)
    basic_comp.append(basic_c)
    complex_comp.append(complex_c)
    nodes.append(len(graph))
    edges.append(edge_c)
    dependencies.append(depend_c)
    indexing.append(index_c)

    # remove the nodes that have children
    # remain nodes are leaves
    start = set()
    for node, v in graph.iteritems():
      if len(v) == 0 or len(v) == 1 and len(parents) == 0:
        start.add(node)
      for parents, dep in v:
        for p in parents:
          if p in leaves:
            leaves.remove(p)
          if str(p).isdigit():
            start.add(p)
    # dfs    
    reverse_graph = {}
    for node, v in graph.iteritems():
      for parents, dep in v:
        for p in parents:
          if not p in reverse_graph:  
            reverse_graph[p] = set()
          reverse_graph[p].add(node)
    layers.append(dfs(start, leaves, reverse_graph))
    avg_width.append(nodes[-1] / layers[-1]) 
          
mtx = [nodes, params, dataparams, otherparams, indexedparams, edges, dependencies, numpy.add(basic_comp, complex_comp), basic_comp, complex_comp, numpy.add(discrete, continuous), discrete, continuous]
labels = ['nodes', 'params', 'dataparams', 'otherparams', 'indexedparams','edges', 'dependencies', 'computations', 'basic_comp', 'complex_comp', 'distributions', 'discrete', 'continuous']
print 'names = ' + str(names)
print 'nodes = ' + str(nodes)
print 'edges = ' + str(edges)
print 'layers = ' + str(layers)
print 'avg_width = ' + str(avg_width)
print 'dependencies = ' + str(dependencies)
print 'params = ' + str(params)
print 'dataparams = ' + str(dataparams)
print 'otherparams = ' + str(otherparams)
print 'indexedparams = ' + str(indexedparams)
#print 'basic_comp = ' + str(basic_comp)
#print 'complex_comp = ' + str(complex_comp)
print 'indexing = ', str(indexing)
print 'computations = ' + str(list(numpy.add(basic_comp, complex_comp)))
for k in level:
  print k + '_comp = ' + str(computations[k])
  mtx.append(computations[k])
  labels.append(k)
print 'distributions = ' + str(list(numpy.add(discrete, continuous)))
print 'discrete = ' + str(discrete)
print 'continuous = ' + str(continuous)
mtx.append(layers)
labels.append('layers')
mtx = numpy.array(mtx)
print mtx.shape
corr = numpy.corrcoef(mtx)
s = '['
for i in range(len(labels)):
  s += '['
  for j in range(len(labels)):
    s += str(corr[i][j]) + ','
  s += '],\n'
s += ']\n'
print s
print labels

size = list(numpy.add(nodes, dependencies))
ind = size.index(min(size))
size[ind] = 9999

while indexedparams[ind] == 0:
  ind = size.index(min(size))
  size[ind] = 9999
print names[ind], indexedparams[ind]

