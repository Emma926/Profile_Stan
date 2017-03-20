# deal with one statement in multiple lines
# ignore comments
from functions import *
data_type = ['cov_matrix', 'corr_matrix', 'cholesky_factor_cov', 'cholesky_factor_corr', 'unit_vector','ordered','positive_ordered', 'simplex','real', 'int', 'vector', 'row_vector', 'matrix']
op_signs = ['%', '^', ':', ',', '.*', './', '+=', '-=', '/=', '*=', '+', '-', '/', '*', '<=', '<', '>=', ">", '==', '!=', '!', '&&', '||', '\\']
def hasfunction(line):
    for i in line:
      if i in functions:
        return True
    return False

def preprocess(model, printresult = 0):
    # if a line does not have key words, = or ~, combine it with previous line
    lines = []
    ignore = 0
    incomplete_flag = 0
    for line in model:
      line = line.strip('\n').strip(' ')
      if "*/" in line:
        ignore = 0
        continue
      if line == '' or ignore == 1:
        continue
      if line.strip(' ')[0] == '/' and line.strip(' ')[1] == '/':
        continue
      if line.strip(' ')[0] == '#':
        continue
      if '//' in line:
        line = line.split('//')[0].strip(' ')  
      if '#' in line:
        line = line.split('#')[0].strip(' ')
      if '/*' in line:
        ignore = 1
        continue
  
      line = line.replace('<-', "=")
      if '{' in line and not ' {' in line:
        line = line.replace('{', ' {')

      newline = " ".join(line.strip('\n').strip(' ').replace(';', ' '). \
      replace(",", " ").replace(":", " "). \
      replace("[", " ").replace("]", " "). \
      replace('+',' '). \
      replace('.*',' '). \
      replace('<-', ' ').\
      replace('-', ' '). \
      replace('/', ' '). \
      replace('*',' '). \
      replace('!',' '). \
      replace('^',' '). \
      replace('(', ' ( '). \
      replace(')', ' ) '). \
      replace('\'',' '). \
      replace('<',' ').replace('>', ' ').split()).split(' ')
      
      def has_datatype(line):
        for i in data_type:
          if i in line:
            return True
        return False
      
      # declaration, delete <> and contents in between
      if newline[0] in data_type and '<' in line and '>' in line:
        ind_a = line.index('<')
        ind_b = line.index('>')
        line = line[0:ind_a] + line[ind_b+1:]

      if printresult == 1:
        print line
      open_c = line.count('(')
      close_c = line.count(')')
      if open_c < close_c:
        if printresult == 1:
          print 'END incomplete'
        incomplete_flag = 0
        lines[-1] = lines[-1].strip('\n') + ' ' + line.strip(' ')
      elif close_c > open_c:
        if printresult == 1:
          print 'BEGIN incomplete'
        incomplete_flag = 1
        lines.append(line)
      elif 'increment_log_prob' == newline[0]:
        lines.append('target = ' + line)  
      elif incomplete_flag == 1:
        lines[-1] = lines[-1].strip('\n') + ' ' + line.strip(' ')
      elif has_datatype(newline) \
      or 'for' in newline \
      or 'if' in newline \
      or 'else' in newline \
      or 'return' in newline \
      or '{' in newline \
      or '}' in newline \
      or '=' in newline \
      or '~' in newline:
      #or hasfunction(newline) and not (line[0] in op_signs or lines[-1][-1] in op_signs):
        lines.append(line)
  
      else:
        lines[-1] = lines[-1].strip('\n') + ' ' + line.strip(' ')
  
    if printresult == 1:
      print '\nAfter preprocess: '
      for line in lines:
        print line
    return lines
