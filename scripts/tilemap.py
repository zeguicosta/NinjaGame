import pygame

# Defines the 9 tiles around the player, including the middle one
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
# Tiles that have physics enabled
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size = 16):
        # Taking the game parameter, so we can use the assets that have been set there
        # self.game gets the game parameter as its value so we can use it on this class
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        # Images rendered off the grid
        self.offgrid_tiles = []

        for i in range(10):
            # str to convert the number that is being added to 'i' to this -> 4;10 (position x=4, y=10)
            # Starts on x=3, and has the y pos locked on 10 (horizontal line)
            # 'type': 'grass' -> Looking up a value in a dictionary
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    # Checks the collision of 9 tiles around the player, including the middle one, so we don't have to check all of them
    def tiles_around(self, pos):
        tiles = []
        # Converts the pixel position into a grid position
        # Isso é feito dividindo as coordenadas de pos pelo tamanho de um tile (self.tile_size), o que indica quantos 
        # tiles se encaixam nessas coordenadas a partir da origem do mapa.
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            # Checks if there is actually a tile on that space or if it is just empty
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        # Retorna a lista tiles com todos os tiles encontrados
        return tiles

    # Filters the nearby tiles for things that have physics enabled 
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                # Creates a collision rectangle for the tile (tile x pos, tile y pos, tile x size, tile y size)
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surf, offset=(0, 0)):
        # Renders the offgrid tiles
        for tile in self.offgrid_tiles:
            # (tile['pos] - offset) makes the camera works
            # if the camera goes to the right, everything else moves to the left
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # Renders the tilemap
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            # Sets the [type and variant], and then (x pos * tile size, y pos * tile size)
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
