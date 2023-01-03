#!/usr/bin/env python
'''
  add some falling snow
'''

import argparse
import logging
import os
import random
import sys

from PIL import Image


def animate(image, snowflakes, frames=200, speed=6, n_flakes=50):
  logging.info('starting...')
  base = Image.open(image)
  width, height = base.size

  pos = []
  for _ in range(n_flakes): # each flake
    x = random.randrange(width)
    y = random.randrange(height)
    sp = random.randrange(int(speed / 2), speed * 2)
    size = random.randrange(16,96)
    flake = Image.open(snowflakes[random.randrange(len(snowflakes))]).resize((size,size))
    pos.append((x,y,sp,flake))

  for frame in range(frames): # each frame
    base = Image.open(image)
    for idx in range(n_flakes): # each flake
      base.paste(pos[idx][3], (int(pos[idx][0]), int(pos[idx][1])), pos[idx][3].convert('RGBA'))
      # move down
      x = (pos[idx][0] + random.randrange(-5, 5) ) % width
      y = (pos[idx][1] + pos[idx][2] ) % height
      pos[idx] = (x, y, pos[idx][2], pos[idx][3])
    # save frame
    base.save('snow.{:03d}.jpg'.format(frame), quality=95)
    logging.debug('wrote %i', frame)

  # generate a movie
  os.system('ffmpeg -r 24 -i snow.%03d.jpg -crf 18 -preset slow -vf scale=1080:-1 -c:v libx264 -pix_fmt yuv420p snow.mp4')
  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Add falling snow')
  parser.add_argument('--image', required=True, help='source image')
  parser.add_argument('--snowflakes', required=True, nargs='+', help='snowflake images')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  animate(args.image, args.snowflakes)
