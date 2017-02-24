import os

root = '/Users/emma/Projects/Bayesian/profiling/stan_BPA/code'
out_path = '/Users/emma/Projects/Bayesian/profiling/stan_BPA/outputs/rprof'
paths = []
# find all the paths
files = os.listdir(root)
for f in files:
    if 'Ch' in f:
      paths.append(os.path.join(root, f))

tool = 'rscript '
head = 'Rprof(\'rprof.out\')\n'
tail = '\nRprof(NULL)\nsummaryRprof()\n'
for path in paths:
  os.chdir(path)
  files = os.listdir('.')
  for f in files:
    if not ('.R' in f and not '.data.R' in f):
      continue
    name = f.replace('.R', '')
    fin = open(f, 'r')
    fout = open('tmp.R', 'w')
    
    for line in fin:
      if 'library(rstan)' in line:
        fout.write(line)
        fout.write(head)
      else:
        fout.write(line)
    fout.write(tail)
    fout.close()
    fin.close()
    command = tool + 'tmp.R > ' + name + '.rprof\n'
    os.system(command)
    print(os.path.join(path,f))
    os.system('mv ' + name + '.rprof ' + out_path)   
    os.system('rm rprof.out')
    os.system('rm tmp.R')
