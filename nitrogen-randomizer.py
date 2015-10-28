#!/usr/bin/env python3
import os
import glob
import argparse
import configparser
import time
import random
from subprocess import call

parser = argparse.ArgumentParser(description="Wallpaper randomizer for nitrogen")
parser.add_argument("--nitrogen-config-dir", "-c",
                    help="Configuration directory used by nitrogen (defaults to ~/.config/nitrogen)",
                    default="~/.config/nitrogen")
parser.add_argument("--interval", "-i", help="Change interval in seconds (defaults to 300)", default=300)
parser.add_argument("--once", help="Only set the wallpapers once and then exit", action="store_true", default=False)
parser.add_argument("wallpaperpool", help="Directory containing the wallpapers")
args = parser.parse_args()


def swap_wallpapers(config_dir, wallpaper_dir):
    wallpapers = list(glob.glob(wallpaper_dir + "/*"))
    random.shuffle(wallpapers)

    nitrogen_config = configparser.ConfigParser()
    nitrogen_config.read(os.path.join(config_dir, "bg-saved.cfg"))

    monitors = nitrogen_config.sections()
    for monitor in monitors:
        nitrogen_config[monitor]["file"] = wallpapers[0]
        wallpapers = wallpapers[1:]
    with open(os.path.join(config_dir, "bg-saved.cfg"), "w") as configfile:
        nitrogen_config.write(configfile)

    call(["nitrogen", "--restore"])


if __name__ == "__main__":
    config_dir = os.path.expanduser(args.nitrogen_config_dir)
    wallpaper_pool = os.path.expanduser(args.wallpaperpool)
    swap_wallpapers(config_dir, wallpaper_pool)
    while not args.once:
        try:
            time.sleep(args.interval)
            swap_wallpapers(config_dir, wallpaper_pool)
        except KeyboardInterrupt:
            break
