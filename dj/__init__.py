#!/usr/bin/env python

import tempfile
import subprocess
import os
import sys
import pipes
import json

ESSENTIA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'essentia_streaming_extractor_freesound'))

# Lookup of Raw Essentia Key to Simplified
KEY_LOOKUP = {
  "AMAJOR": "A",
  "AMINOR": "Am",
  "A#MAJOR": "Bb",
  "A#MINOR": "Bbm",
  "BBMAJOR": "Bb",
  "BBMINOR": "Bbm",
  "BMAJOR": "B",
  "BMINOR": "Bm",
  "CMAJOR": "C",
  "CMINOR": "Cm",
  "C#MAJOR": "Db",
  "C#MINOR": "Dbm",
  "DBMAJOR": "Db",
  "DBMINOR": "Dbm",
  "DMAJOR": "D",
  "DMINOR": "Dm",
  "D#MAJOR": "Eb",
  "D#MINOR": "Ebm",
  "EBMAJOR": "Eb",
  "EBMINOR": "Ebm",
  "EMAJOR": "E",
  "EMINOR": "Em",
  "FMAJOR": "F",
  "FMINOR": "Fm",
  "F#MAJOR": "F#",
  "F#MINOR": "F#m",
  "GBMAJOR": "F#",
  "GBMINOR": "F#m",
  "GMAJOR": "G",
  "GMINOR": "Gm",
  "G#MAJOR": "Ab",
  "G#MINOR": "Abm",
  "ABMAJOR": "Ab",
  "ABMINOR": "Abm",
  ###
  "AMAJ": "A",
  "AMIN": "Am",
  "A#MAJ": "Bb",
  "A#MIN": "Bbm",
  "BBMAJ": "Bb",
  "BBMIN": "Bbm",
  "BMAJ": "B",
  "BMIN": "Bm",
  "CMAJ": "C",
  "CMIN": "Cm",
  "C#MAJ": "Db",
  "C#MIN": "Dbm",
  "DBMAJ": "Db",
  "DBMIN": "Dbm",
  "DMAJ": "D",
  "DMIN": "Dm",
  "D#MAJ": "Eb",
  "D#MIN": "Ebm",
  "EBMAJ": "Eb",
  "EBMIN": "Ebm",
  "EMAJ": "E",
  "EMIN": "Em",
  "FMAJ": "F",
  "FMIN": "Fm",
  "F#MAJ": "F#",
  "F#MIN": "F#m",
  "GBMAJ": "F#",
  "GBMIN": "F#m",
  "GMAJ": "G",
  "GMIN": "Gm",
  "G#MAJ": "Ab",
  "G#MIN": "Abm",
  "ABMAJ": "Ab",
  "ABMIN": "Abm",
  ###
  "A": "A",
  "AM": "Am",
  "BB": "Bb",
  "BBM": "Bbm",
  "BB": "Bb",
  "BBM": "Bbm",
  "B": "B",
  "BM": "Bm",
  "C": "C",
  "CM": "Cm",
  "DB": "Db",
  "DBM": "Dbm",
  "DB": "Db",
  "DBM": "Dbm",
  "D": "D",
  "DM": "Dm",
  "EB": "Eb",
  "EBM": "Ebm",
  "EB": "Eb",
  "EBM": "Ebm",
  "E": "E",
  "EM": "Em",
  "F": "F",
  "FM": "Fm",
  "F#": "F#",
  "F#M": "F#m",
  "F#": "F#",
  "F#M": "F#m",
  "G": "G",
  "GM": "Gm",
  "AB": "Ab",
  "ABM": "Abm",
  "AB": "Ab",
  "ABM": "Abm"
}

def sys_exec(cmd):
  """
  Run a shell command.
  """
  class _proc(object):

    def __init__(self, command):
      self.command = command
      self._stdin = None
      self._stdout = None
      self._stdout_text = None
      self._returncode = None

    def set_stdin(self, stdin):
      self._stdin = stdin

    def set_stdout(self, stdout):
      self._stdout = stdout

    @property
    def stdin(self):
      return 'stdin'

    @property
    def stdout(self):
      if self._stdout_text is not None:
        return self._stdout_text

    @property
    def stderr(self):
      if self._stderr_text is not None:
        return self._stderr_text

    @property
    def returncode(self):
      if self._returncode is not None:
        return self._returncode

    @property
    def ok(self):
      if self._returncode is not None:
        return self.returncode is 0

    @property
    def subprocess(self):
      if self._subprocess is not None:
        return self._subprocess

    def start(self):
      self._subprocess = subprocess.Popen(
        args=self.command,
        shell=True,
        stdin=self._stdin if self._stdin else subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
      )

    def wait(self, unread=False):
      self._returncode = self._subprocess.wait()
      if self._subprocess.stdout is not None and not unread:
        self._stdout_text = self._subprocess.stdout.read().decode()
        self._stderr_text = self._subprocess.stderr.read().decode()

    def run(self):
      self.start()
      self.wait()

    def __repr__(self):
      return '<Process: {0}>'.format(self.command)

  p = _proc(cmd)
  p.run()
  return p

def main():

  if not len(sys.argv) == 2:
    sys.stderr.write("Usage: dj <file>\n")
    sys.exit(1)

  # make temp file root
  fp_root = tempfile.mktemp(suffix='dj-temp')
  fp_stats = fp_root + "_statistics.json"
  fp_frames = fp_root + "_frames.json"

  # cmd
  cmd = '{0} {1} "{2}"'.format(ESSENTIA_PATH, pipes.quote(sys.argv[1]), fp_root)

  # exec
  proc = sys_exec(cmd)
  if not proc.ok:
    raise RuntimeError("Error running: {0}\nSTDOUT:\n{1}\nSTDERR:\n{2}".format(cmd, proc.stdout, proc.stderr))

  # load output
  data = json.load(open(fp_stats))

  # remove
  try:
    os.remove(fp_stats)
    os.remove(fp_frames)
  except:
    pass
  attrs = {}
  attrs["bpm"] = round(data.get("rhythm",{}).get("bpm", 0), 1)
  attrs["key"] = KEY_LOOKUP.get((data.get("tonal", {}).get("key_key", "") + data.get("tonal", {}).get("key_scale", "")).upper(), None)
  sys.stdout.write(json.dumps(attrs) + "\n")

if __name__ == '__main__':
  main()