from basketball import models as bmodels
from django.conf import settings
import os, sys

players = bmodels.Player.objects.all()

for player in players:

    try:
        original_path = player.image_src.path
    except:
        print(player.first_name + ' ' + player.last_name)
        continue
    new_file_path = settings.MEDIA_ROOT + 'player_images/' + str(player.id) + '/'
    if not os.path.isdir(new_file_path):
        os.makedirs(new_file_path)
    new_file_path += player.image_src.name.split('/')[-1]

    os.rename(original_path, new_file_path)
    player.image_src.name = 'player_images/' + str(player.id) + '/' + player.image_src.name.split('/')[-1]
    player.save()
