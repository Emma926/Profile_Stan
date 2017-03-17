# Graphical Model Profiling Tools
This tool converts stan model file as input, output variable dependencies as graph structure.

## Getting Start
modify model_parser_wrapper.py as needed, and run
'''
python model_parser_wrapper.py
'''
## Probabilistic Graph Data Structure
parse_model.py stores probability graph ending with .probgraph.
It streams graph into a json file.
The data structure is:
* {node: [([parents], dependency_type)]}
where 
* dependency_type:
  + indexing, 
  + simple/complex computation,
  + discrete/continuous distribution




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
10. the dependency belongs to complex
11. (a more sophisticated way to solve this is to build a graph for each functions, and map variables accordingly whenever the function is called)
12.  works for 69 model files in BPA, verified 17 files
13.  variables assigned within if statement, are dependent on the variables in if conditions. Dependency type is basic.
14.  variables declared within for loops, are dependent on the loop indices; the dependency is indexing
15.  we add indexing dependency for one variable at a time. For example (['a', 'b'], 'indexing') should be converted to (['a'], 'indexing'), (['b'], 'indexing')
16.  does not work for for statement without {} followed by more than one statement, example:
    28   for (n in 1:nmax)
    29     if (n < nmin)
    30       lp_parts[n] <- log(1.0 / nmax) + negative_infinity();  // Zero probability
    31     else
    32       lp_parts[n] <- log(1.0 / nmax) + binomial_log(k, n, theta);
17.  does not work for if/for statements, whoes { is in a new line


Emma Wang
Originally on Feb 24th, 2017,
Updated on March 17th, 2017.
