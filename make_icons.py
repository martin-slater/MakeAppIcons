#!/bin/python
# pylint: disable=too-few-public-methods, missing-docstring, C0413
# -----------------------------------------------------------------------------
# Darkstorm Library
# Copyright (C) 2021 Martin Slater
# Created : Wednesday, 01 December 2021 09:06:27 AM
# -----------------------------------------------------------------------------
"""
MapCreate command line tool.
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import argparse
import os
import shutil
import sys

from PIL import Image

# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------

UWPIconSet = {
    'OutputFolder':  'UWP',
    'Files': {
        "Assets": [
            ('LargeTile.scale-100.png', (310, 310)),
            ('LargeTile.scale-200.png', (620, 620)),
            ('LargeTile.scale-400.png', (1240, 1240)),
            ('SmallTile.scale-100.png', (71, 71)),
            ('SmallTile.scale-200.png', (142, 142)),
            ('SmallTile.scale-400.png', (284, 284)),
            ('SplashScreen.scale-100.png', (620, 300)),
            ('SplashScreen.scale-200.png', (1240, 600)),
            ('SplashScreen.scale-400.png', (2480, 1200)),
            ('Square150x150Logo.scale-100.png', (150, 150)),
            ('Square150x150Logo.scale-200.png', (300, 300)),
            ('Square150x150Logo.scale-400.png', (600, 600)),
            ('Square44x44Logo.altform-unplated_targetsize-16.png', (16, 16)),
            ('Square44x44Logo.altform-unplated_targetsize-48.png', (48, 48)),
            ('Square44x44Logo.altform-unplated_targetsize-256.png', (256, 256)),
            ('Square44x44Logo.scale-100.png', (44, 44)),
            ('Square44x44Logo.scale-200.png', (88, 88)),
            ('Square44x44Logo.scale-400.png', (176, 176)),
            ('Square44x44Logo.targetsize-16.png', (16, 16)),
            ('Square44x44Logo.targetsize-48.png', (48, 48)),
            ('Square44x44Logo.targetsize-256.png', (256, 256)),
            ('StoreLogo.scale-100.png', (50, 50)),
            ('StoreLogo.scale-200.png', (100, 100)),
            ('StoreLogo.scale-400.png', (200, 200)),
            ('Wide310x150Logo.scale-100.png', (310, 150)),
            ('Wide310x150Logo.scale-200.png', (620, 300)),
            ('Wide310x150Logo.scale-400.png', (1240, 600)),
        ]
    }
}

IOSIconSet = {
    'OutputFolder': 'IOS',
    'Files': {
        "Resources": [
            ('Default.png', (320, 480)),
            ('Default@2x.png', (640, 960)),
            ('Default-568h@2x.png', (640, 1136)),
            ('Default-Portrait.png', (768, 1004)),
            ('Default-Portrait@2x.png', (1536, 2008)),
            ('xamarin_logo.png', (220, 51)),
            ('xamarin_logo@2x.png', (440, 101)),
            ('xamarin_logo@3x.png', (880, 202)),
        ],
        "Icons": [
            ('Icon1024.png', (1024, 1024)),
            ('Icon120.png', (120, 120)),
            ('Icon152.png', (152, 152)),
            ('Icon167.png', (167, 167)),
            ('Icon180.png', (180, 180)),
            ('Icon20.png', (20, 20)),
            ('Icon29.png', (29, 29)),
            ('Icon40.png', (40, 40)),
            ('Icon58.png', (58, 58)),
            ('Icon60.png', (60, 60)),
            ('Icon76.png', (76, 76)),
            ('Icon80.png', (80, 80)),
            ('Icon87.png', (87, 87)),
        ]
    }
}

Platforms = [
    UWPIconSet,
    IOSIconSet
]


def hex_to_rgba(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 4], 16) for i in range(0, lv, lv // 4))


class MakeIcons(object):
    def __init__(self, args):
        """ Constructor """
        self.source_image = args.source_image
        self.output_dir = args.output_dir
        self.clean_output = args.force
        argb = hex_to_rgba(args.background_color)
        self.background_color = (argb[1], argb[2], argb[3])
        self.alpha = argb[0]

        print(f'Image source     : {self.source_image}')
        print(f'Output directory : {self.output_dir}')

    def run(self):
        if os.path.exists(self.output_dir):
            if self.clean_output:
                shutil.rmtree(self.output_dir, ignore_errors=False)
            else:
                print('Output directory already exists')
                sys.exit()

        os.mkdir(self.output_dir)

        img = Image.open(self.source_image)
        width, height = img.size
        for platform in Platforms:
            platform_dir = os.path.join(
                self.output_dir, platform['OutputFolder'])
            os.mkdir(platform_dir)
            for group_name, group_files in platform['Files'].items():
                group_dir = os.path.join(platform_dir, group_name)
                os.mkdir(group_dir)
                for file in group_files:
                    output_name = os.path.join(group_dir, file[0])
                    out_width, out_height = file[1]

                    scale = out_width / width

                    img_width = (int)(width * scale)
                    img_height = (int)(height * scale)

                    if img_height > out_height:
                        scale = out_height / img_height
                        img_height = (int)(img_height * scale)
                        img_width = (int)(img_width * scale)

                    resized_img = img.resize(
                        (img_width, img_height), resample=Image.ANTIALIAS)

                    background_img = Image.new("RGBA", (out_width, out_height))
                    background_img.paste(
                        self.background_color, (0, 0, background_img.size[0], background_img.size[1]))
                    background_img.putalpha(self.alpha)

                    vpad = (int)((out_height - img_height) / 2)
                    hpad = (int)((out_width - img_width) / 2)

                    temp_img = Image.new("RGBA", (out_width, out_height))
                    temp_img.paste(resized_img, (hpad, vpad))

                    output_img = Image.alpha_composite(
                        background_img, temp_img)

                    output_img.save(output_name)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    """ Main script entry point """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d-', '--output_dir',
                        type=str,
                        help="Output directory",
                        dest="output_dir",
                        action='store')
    parser.add_argument('-s', '--source',
                        type=str,
                        help='Input image file',
                        dest='source_image',
                        action='store')
    parser.add_argument('-f', '--force',
                        help='Remove all existing files under the output directory',
                        dest='force',
                        action='store_true')
    parser.add_argument('-c', '--color',
                        help='Background color',
                        dest='background_color',
                        default='#00000000',
                        action='store')
    args = parser.parse_args()
    MakeIcons(args).run()


if __name__ == "__main__":
    main()
