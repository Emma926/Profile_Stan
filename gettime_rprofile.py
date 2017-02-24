import os

output_path = "/Users/emma/Projects/Bayesian/profiling/stan_BCM/outputs/rprof"

files = os.listdir(output_path)
os.chdir(output_path)

names = []
inference_time = []
sampling_time = []
total_time = []
for f in files:
  if not '.rprof' in f:
    continue
  fin = open(f, 'r')
  totaltime = 0
  time = 0
  start = 0
  flag = 0
  s_time = 0 # sampling percentage
  i_time = 0 # inference percentage
  for line in fin:
    if "$by.total" in line:
      start = 1
    if start == 1:
      newline = ' '.join(line.split())
      if '\"stan\"' in line:
        i_time = float(newline.strip('\n').split(' ')[2])
        inference_time.append(i_time)
        flag = 1
        t_time = float(newline.strip('\n').split(' ')[1])
        total_time.append(t_time*100/i_time)
      if "\"sampling\"" in line:
        s_time = float(newline.strip('\n').split(' ')[2])
        sampling_time.append(s_time)
        flag = 2
  if flag == 0:
    print f, '!'
  else:
    names.append(f.split('.')[0])
      

new_sampling = []
for i in range(len(sampling_time)):
    new_sampling.append(sampling_time[i] / inference_time[i])

print names
print inference_time
print sampling_time
print total_time
print new_sampling
print len(names), len(inference_time), len(sampling_time), len(total_time)
