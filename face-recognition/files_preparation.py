import os, re
from shutil import copyfile

for filename in os.listdir(os.getcwd() + '//sorted_set//'):
    tmp = re.compile('subject(.*)\.(.*)')
    m = tmp.match(filename)
    if not os.path.exists(os.getcwd() + '//sorted_set//' + m.group(2) + '//'):
        os.makedirs(os.getcwd() + '//sorted_set//' + m.group(2) + '//')
    copyfile(os.getcwd() + '//sorted_set//' + filename,
             os.getcwd() + '//sorted_set//' + m.group(2) + '//' + m.group(1) + '.gif')
