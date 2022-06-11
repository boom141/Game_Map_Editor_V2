import pygame,os

class TILE_LIST_LOADER:
    def __init__(self):
        self.Tiles = []

    def Load_Tiles(self,folder_n,file_n,length):
        for i in range(length):
            self.Tiles.append(pygame.image.load(os.path.join(folder_n, f'{file_n}{i}.png')))
        return self.Tiles