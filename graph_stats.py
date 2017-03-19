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
params = []
dataparams = []

for graphfile in files:
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

print names
print params
print dataparams
