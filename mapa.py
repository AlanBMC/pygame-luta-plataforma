
from globais import *
import pygame
from pytmx.util_pygame import load_pygame
import pytmx

def desenha_mapa(surface, tm, camera_x, camera_y, scale=1):
    tw = int(tm.tilewidth * scale)
    th = int(tm.tileheight * scale)

    start_x = max(0, int(camera_x / tw))
    end_x = min(start_x + int(surface.get_width() / tw) + 1, tm.width)
    start_y = max(0, int(camera_y / th))
    end_y = min(start_y + int(surface.get_height() / th) + 1, tm.height)

    for layer in tm.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
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



