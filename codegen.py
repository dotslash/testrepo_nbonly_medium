import sys
from pathlib import Path
import uuid

def make_command(ssize=1000):
  rand_str = lambda: uuid.uuid4().hex
  len_rand_str = len(rand_str())
  ret = [rand_str() for i in range(ssize//len_rand_str)]
  all_lines = '\n'.join(ret)
  content = f'"""\n{all_lines}\n"""\n'
  return "# COMMAND ----------\n" + content 

def make_notebook():
  part1 = "# Databricks notebook source"
  part2 = "".join((make_command(ssize=200) for _ in range(30)))
  return part1 + "\n" + part2

def make_file():
  return make_command()

if __name__ == '__main__':
  nfiles = int(sys.argv[1])
  nb_ok, files_ok = True, True
  assert sys.argv[2] in ("files_only", "nb_only", "files_and_nb")
  if sys.argv[2] == "files_only": nb_ok = False
  if sys.argv[2] == "nb_only": files_ok = False

  for i in range(nfiles):
    if i%10 < 2 and nb_ok:
      # 123 => 1/2/3_nb.py
      fname = '/'.join(list(str(i)))
      fname = f"{fname}_nb.py"
      p = Path(fname)
      p.parent.mkdir(exist_ok=True)
      p.write_text(make_notebook())
    elif i%10 >= 2 and files_ok:
      # 123 => 1/2/3.txt
      fname = '/'.join(list(str(i)))
      fname = f"{fname}.txt"
      p = Path(fname)
      p.parent.mkdir(exist_ok=True)
      p.write_text(make_file())

