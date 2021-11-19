#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import pathlib
import os
import sys

def generate_video_output_filename(in_filename, out_directory):
  filename = os.path.basename(in_filename)
  filename = pathlib.Path(filename)
  filename = filename.with_suffix('.mp4')
  return os.path.join(out_directory, filename)

def encode_video_with_subs(in_filename, out_directory):
  out_filename = generate_video_output_filename(in_filename, out_directory)
  basename = os.path.basename(in_filename)

  try:
    out, err = (
      ffmpeg
        .input(in_filename)
        .output(
          out_filename,
          preset='medium', movflags='+faststart',
          # vcodec='copy',
          vcodec='libx264', level='3.1', crf='23',
          acodec='copy',
          vf='subtitles=\'%s\'' % in_filename,
        )
        .overwrite_output()
        .run(quiet=True)
    )
  except ffmpeg.Error as e:
    print(e.stderr, file=sys.stderr)
    sys.exit(1)

  return out

parser = argparse.ArgumentParser(description="Encode to iOS format")
parser.add_argument('in_directory', help='Input directory')
parser.add_argument('out_directory', help='Output "encoded" directory')

if __name__ == '__main__':
  args = parser.parse_args()

  count = 0

  in_directory = os.path.abspath(args.in_directory)
  out_directory = os.path.abspath(args.out_directory)

  for filename in os.listdir(in_directory):
    if filename.endswith('.mkv'):
      in_filename = os.path.join(in_directory, filename)
      out = encode_video_with_subs(in_filename, out_directory)
      count += 1

  print("yep: %d" % count)
