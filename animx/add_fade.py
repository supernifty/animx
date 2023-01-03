#!/usr/bin/env python
'''
  fade an image
'''

import argparse
import logging
import os
import random
import sys

from PIL import Image
from PIL import ImageEnhance


def animate(image, frames=10):
  logging.info('starting...')
  base = Image.open(image)
  width, height = base.size
  prefix = image.split('.')[0]

  for frame in range(frames): # each frame
    tx = 1 - frame/frames
    base = Image.open(image)
    enhancer = ImageEnhance.Brightness(base)
    darker_image = enhancer.enhance(tx)
    # save frame
    darker_image.save('{}.{:03d}.png'.format(prefix, frame), quality=95)
    logging.debug('wrote %i', frame)

  #os.system('ffmpeg -r 24 -i snow.%03d.jpg -crf 18 -preset slow -vf scale=1080:-1 -c:v libx264 -pix_fmt yuv420p snow.mp4')
  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Fade an image to black')
  parser.add_argument('--image', required=True, help='source image')
  parser.add_argument('--frames', required=False, type=int, default=10, help='number of frames to write')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  animate(args.image, args.frames)
