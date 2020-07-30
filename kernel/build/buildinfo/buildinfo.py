"""Buildinfo.py.

Produce the list of translation units and their compiler flags this kernel
was built with.

Parses *.o.cmd files produced in the env var $OUT_DIR.

Produces JSON in the form:
{
    "<absolute path to *.c source file>": [
        "-I<absolute path to include dir>",
        "-D<symbol definition>",
        "<other flags that affect what gets included>",
        ...
    ],
    ...
}

This is immediately useful for static analysis tools.  The list of translation
units speeds up analysis by only looking at files included in this build.  The
includes and defines flag gives us information required for producting a
correct AST.

usage: ROOT_DIR=/path/to/kernel KERNEL_DIR=private/<chipset>-<vendor> \
       OUT_DIR=/path/to/out/branch/ python buildinfo.py
"""

import json
import os
import subprocess


def find_cmd_files():
  return subprocess.check_output(
      ["find", os.environ["OUT_DIR"], "-name", "*.o.cmd"]).split("\n")


def parse_cmd_files(cmds):
  flags = {}
  for cmd in cmds:
    f, cla = parse_cmd_file(cmd)
    if f and f.endswith(".c") and cla:
      flags[f] = cla
  return flags


def make_abs(s):
  if s[2] != os.sep:
    return [
        "-I" + os.path.join(os.environ["OUT_DIR"], s[2:]),
        "-I" + os.path.join(os.environ["ROOT_DIR"], os.environ["KERNEL_DIR"],
                            s[2:])
    ]
  return [s]


def filter_flags(all_flags):
  flags = []
  for i, flag in enumerate(all_flags):
    if flag.startswith("-D") or flag == "-nostdinc":
      flags.append(flag)
    elif flag.startswith("-I"):
      flags.extend(make_abs(flag))
    elif flag == "-include" or flag == "-isystem":
      flags.extend(all_flags[i:i + 2])
  return flags


def parse_cmd_file(cmd):
  if not cmd:
    return (None, None)
  with open(cmd) as fp:
    contents = fp.readline().split(" ")
    filename = contents[-1].rstrip()
    return (filename, filter_flags(contents))


def write_out(db):
  path = os.path.join(os.environ["OUT_DIR"], "compile.json")
  with open(path, "w") as fp:
    json.dump(db, fp, indent=4, separators=(",", ": "))

if __name__ == "__main__":
  write_out(parse_cmd_files(find_cmd_files()))
