
from globais import *
#from variaveis_gravidade_pulo import *
import pygame
from pytmx.util_pygame import load_pygame
import pytmx






def desenha_mapa(surface, tm, camera_x, camera_y, scale=1):
    tw = int(tm.tilewidth * scale)
    th = int(tm.tileheight * scale)
    map_width = tm.width * tw
    map_height = tm.height * th

    # Limitar a câmera dentro dos limites do mapa
    camera_x = max(0, min(camera_x, map_width - surface.get_width()))
    camera_y = max(0, min(camera_y, map_height - surface.get_height()))

    start_x = int(camera_x / tw)
    end_x = start_x + int(surface.get_width() / tw) + 1  # +1 para cobrir casos de borda
    start_y = int(camera_y / th)
    end_y = start_y + int(surface.get_height() / th) + 1  # +1 para cobrir casos de borda

    for layer in tm.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x in range(start_x, min(end_x, layer.width)):
                for y in range(start_y, min(end_y, layer.height)):
                    gid = layer.data[y][x]
                    tile = tm.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (tw, th))
                        surface.blit(tile, ((x * tw) - camera_x, (y * th) - camera_y))




def carrega_mapa(filename):
    tm = load_pygame(filename)

    tm.colisor_pisos_chao = []
    collision_layer = tm.get_layer_by_name("pisos_chao")
    for x, y, gid in collision_layer:
        if gid:
            rect = pygame.Rect(x * tm.tilewidth, y *
                               tm.tileheight, tm.tilewidth, tm.tileheight)
            tm.colisor_pisos_chao.append(rect)

    return tm
