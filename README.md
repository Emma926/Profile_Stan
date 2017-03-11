# Graphical Model Profiling Tools

This project contains the following files:
  - parse_model.py:       compile stan model into graphical representation
  - rprof_totaltime.py:   run BPA examples with rprof, save the outputs
  - gettime_rprofile.py:  parse output files generated by rprof, summarize total runtime ect.
  - plot.ipynb:           plot total runtime etc.

## Probability Graph Data Structure
  parse_model.py stores probability graph ending with .probgraph.
  It streams graph into a json file.
  The data structure is:
    {node: [([parents], dependency_type)]}
  where 
    dependency_type:
      indexing, 
      simple/complex computation,
      discrete/continuous distribution




## CAVEAT
1.  variables are dependent on the index variables 
2.  real beta[3]; there are 3 betas here, create "3" as a "variable"; only keep the largest integer
3.  ignore the arithmetic operations within []
4.  examples: eps[2:nyear] = eps2[1:nyear - 1], or N_est[t + 1] = N_est[t] * lambda[t];
5.  a[b[i],c[i]], generate i->b, i->c, b->a, c->a (ignore i->a)
6.  verified 14 models out of 69 models in BPA
7.  does not work for one statement with {} in one line
8.  does not support /* or */ appearing after statements
9.  simply deal with functions{} (e.g. Ch.07/cjs_add.stan) by adding a connection between returned value and arguments
10. a more sophisticated way to solve this is to build a graph for each functions, and map variables accordingly whenever the function is called
11.  works for 69 model files in BPA, verified 17 files


Emma Wang
Originally on Feb 24th, 2017
Updated on March 7th, 2017