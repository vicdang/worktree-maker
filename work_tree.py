# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
---------------------------
Copyright (C) 2022
@Authors: dnnvu.menlo
@Date: 30-Dec-22
@Version: 1.0
---------------------------
 Usage example:
   - work_tree.py <options>

"""
import argparse
import json
import logging
import re
import os
import shutil
import signal
import sys

from anytree import Node, RenderTree

log = logging.getLogger(__name__)

class WorkTree(object):
   """docstring for WorkTree"""

   def __init__(self, args):
      super(WorkTree, self).__init__()
      self.data_file = args.data_file
      self.year = args.year
      self.data = {}
      self.dirs = []
      self.mode = 0o666
      self.tmp_file = 'template.docx'
      self.form = '/InterviewForm_(FullName)_(Position).docx'
      self.curr_dir = './'

   def generate_path(self):
      """
      Generate path
      """
      # path = os.path.join(curr_dir, p)
      for p in self.generate_worktree():
         path = self.curr_dir + str(p)
         log.debug("Making : %s" % path)
         try:
            os.makedirs(path, self.mode)
         except Exception as err:
            log.error(err)
         try:
            shutil.copyfile(self.tmp_file, path + self.form)
            log.info("Maked : %s" % path)
         except Exception as err:
            log.error(err)

   def generate_worktree(self):
      """
      Generate worktree
      """
      for p in self.decor_worktree():
         yield re.findall("\'.*\'", str(p))[0].replace("'", "")

   def decor_worktree(self):
      parents = [Node(".")]
      for layer in self.data['template']:
         t = []
         for parent in parents:
            for node in self.data['data'][layer]:
               n = Node(node, parent=parent)
               t.append(n)
         parents = t
      return parents

   def get_pattern(self):
      """
      Get data from file
      """
      with open(self.data_file, 'r') as d_file:
         self.data = json.load(d_file)
      return self.data

   def run(self):
      """
      Execute
      """
      self.get_pattern()
      self.generate_worktree()
      self.generate_path()

def parse_args():
   """
   Parse arguments as argument parser object
   :return: Arguments
   """
   parser = argparse.ArgumentParser(description=__doc__.strip(),
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('-y', '--year',
                       default=2022,
                       help='Year')
   parser.add_argument('-f', '--data-file',
                       default='data.json',
                       help='template.json file pattern.')
   parser.add_argument("-d", "--debug", action="store_true", default=False,
                       help="Enable debug messages")
   arguments = parser.parse_args()
   return arguments

def main(args):
   """
   Main process
   """
   worktree = WorkTree(args)
   worktree.run()

def _sigterm_handler(signo, ctx):
   """
   Signal termination handler
   :param signo: signal number
   :param ctx: context
   """
   pass

if __name__ == '__main__':
   arguments = parse_args()
   logging.basicConfig(
      level=logging.DEBUG if arguments.debug else logging.INFO,
      format='[%(asctime)s] {%(pathname)s:%(lineno)d} %('
             'threadName)s %(levelname)s '
             '%(message)s',
      datefmt='%H:%M:%S')
   signal.signal(signal.SIGTERM, _sigterm_handler)
   signal.signal(signal.SIGINT, _sigterm_handler)
   # signal.signal(signal.SIGQUIT, _sigterm_handler)
   main(arguments)
