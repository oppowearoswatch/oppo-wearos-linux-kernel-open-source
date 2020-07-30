#!/usr/bin/python
# Copyright 2017 Google Inc.
# Author: tstrudel@google.com

import subprocess
import sys
import os

if len(sys.argv) != 3:
  print('Usage: {} <sha1..range> <kernel-source-files-list>'.
        format(os.path.basename(sys.argv[0])))
  exit(1)

kernel_files = []
for f in open(sys.argv[2]).read().strip().split('\n'):
  if os.path.isfile(f):
    kernel_files.append(f)

out = subprocess.check_output('git log --oneline {}'.format(sys.argv[1]),
                              shell=True)
for l in out.strip().split('\n'):
  el = l.split(' ', 1)
  files = subprocess.check_output('git log --no-color --oneline --name-status -1 {}'.format(el[0]),
                                  shell=True).strip().replace('M\t','').replace('A\t','').replace('D\t','').split('\n')
  prefix_char = ' '
  used_files = []
  for f in files[1:]:
    if f in kernel_files:
      prefix_char = '*'
      used_files.append(f)
  if el[1].startswith('Linux '):
    print(el[1])
  else:
    print('  {} {}'.format(prefix_char, el[1]))
    if used_files:
      print('      ' + '\n      '.join(used_files))
