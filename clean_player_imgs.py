# Small script that removes unused player images

import os
import django
django.setup()
from basketball import models as bmodels

# find image strings in use
used_imgs = []
for player in bmodels.Player.player_objs.all():
    if player.image_src:
        used_imgs.append(player.image_src.path[-player.image_src.path[::-1].index('/'):])
used_imgs.sort()

# get all current image strings in the player images folder
current_imgs = os.listdir('media/player_images/')
current_imgs.sort()

# find all the images that we are going to keep
keeper_imgs = []
for used_img in used_imgs:
    for current_img in current_imgs:
        if used_img in current_img:
            keeper_imgs.append(current_img)

for current_img in current_imgs:
    if current_img not in keeper_imgs:
        print("Removed " + current_img)
        os.remove('media/player_images/' + current_img)
