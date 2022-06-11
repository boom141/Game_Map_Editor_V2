from Tile_list import*
import pygame, sys, os

pygame.init()

WIN_HEIGHT = 1000
WIN_WIDTH = 1000
WIN_MARGIN_BOTTOM = 450
SNAP = 5
TILE_SIZE = 32

Selected_Tile = -1
Highlight = -1

fps = pygame.time.Clock()
Game_Window = pygame.display.set_mode((800,600))
Canvas = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))

up = False
down = False
left = False
right = False
Tile = True
Decor = False

folder_name = 'set1'
file_name = 'tile'
length = 9

INITIAL_POINT = [0,0]

def Draw_Grid():
   Map_data = []
   for y in range(0,WIN_HEIGHT,TILE_SIZE):
    rows = []
    for x in range(0,WIN_WIDTH,TILE_SIZE):
        rows.append(-1)
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(Canvas, ((255,255,255)), rect, 1)
    Map_data.append(rows)
   
   return Map_data

Map_Data = Draw_Grid()
Decoration_Data = []

def Render_Tile_List():
    Tiles = TILE_LIST_LOADER().Load_Tiles(folder_name,file_name,length)
    Tile_Set = []
    offset = -1
    pygame.draw.rect(Game_Window, ((28,28,28)), (0,WIN_MARGIN_BOTTOM,WIN_WIDTH,200))
    for tile in Tiles:
        offset += 1
        tile.set_colorkey((0, 0, 0))
        Tile_Set.append(Game_Window.blit(pygame.transform.scale(tile,(36,36)),((36 * offset) + 10, WIN_MARGIN_BOTTOM + 50)))
    
    return Tile_Set

def Render_Map(Map_Data,Mouse_Pos):
    for y, col in enumerate(Map_Data):
        for x, row in enumerate(col):
            if row > -1:
                image = pygame.image.load(os.path.join('set1', f'tile{row}.png'))
                image.set_colorkey((0,0,0))
                Canvas.blit(pygame.transform.scale(image,(36,36)),(x*TILE_SIZE, y*TILE_SIZE))
            else:
                pygame.draw.rect(Canvas, ((0,0,0)), (x*TILE_SIZE, y*TILE_SIZE,36,36))
    for data in Decoration_Data:
        image = pygame.image.load(os.path.join('set2', f'deco{data[0]}.png'))
        image.set_colorkey((0,0,0))
        Canvas.blit(image,(data[1],data[2]))

def Check_Duplicate(list,coordinate):
    if coordinate in list:
        return True
    else:
        return False

while True:
    Game_Window.fill('gray')
    Mouse_Clicked = pygame.mouse.get_pressed()
    Mouse_Pos = pygame.mouse.get_pos()
    x = (Mouse_Pos[0] - INITIAL_POINT[0]) // TILE_SIZE
    y = (Mouse_Pos[1] - INITIAL_POINT[1]) // TILE_SIZE

    if Mouse_Pos[1] < WIN_MARGIN_BOTTOM and pygame.MOUSEMOTION:
        if Tile:
            if Mouse_Clicked[0]:
                if Map_Data[y][x] != Selected_Tile:
                    Map_Data[y][x] = Selected_Tile
            if Mouse_Clicked[2]:
                if Map_Data[y][x] > -1:
                    Map_Data[y][x] = -1

        elif Decor and Selected_Tile != -1:
            image = pygame.image.load(os.path.join('set2', f'deco{Selected_Tile}.png'))
            image.set_colorkey((0,0,0))
            x = (Mouse_Pos[0] - (image.get_width()//2)) - INITIAL_POINT[0]
            y = (Mouse_Pos[1]-(image.get_height()//2)) - INITIAL_POINT[1]
            Canvas.blit(image,(x,y))
            if Mouse_Clicked[0]:
                verify = Check_Duplicate(Decoration_Data,[Selected_Tile,x,y])
                if not verify:
                    Decoration_Data.append([Selected_Tile,x,y])
                    
    s_movement = [0,0]
    if up:
        s_movement[1] -= SNAP * 1
    elif down:
        s_movement[1] += SNAP * 1
    elif left: 
        s_movement[0] -= SNAP * 1
    elif right:
        s_movement[0] += SNAP * 1


    INITIAL_POINT[0] -= s_movement[0]
    INITIAL_POINT[1] -= s_movement[1]
    Game_Window.blit(Canvas,(INITIAL_POINT[0],INITIAL_POINT[1]))
    
    Render_Map(Map_Data,Mouse_Pos)
    Tile_Set = Render_Tile_List()
    
    for tile in Tile_Set:
        if tile.collidepoint(Mouse_Pos) and Mouse_Clicked[0]:
            Highlight = Tile_Set.index(tile)
            Selected_Tile = Tile_Set.index(tile)
    #Highlight selected tile
    if Highlight != -1:
        pygame.draw.rect(Game_Window, ((0,255,0)), (Tile_Set[Highlight].x - 2 ,Tile_Set[Highlight].y - 2,40,40), 1)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                Tile = True
                Decor = False
                folder_name = 'set1'
                file_name = 'tile'
                length = 9

            if event.key == pygame.K_2:
                Decor = True 
                Tile = False
                folder_name = 'set2'
                file_name = 'deco'
                length = 9
            

            if event.key == pygame.K_UP:    
                up = True
            if event.key == pygame.K_DOWN:
                down = True
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:    
                up = False
            if event.key == pygame.K_DOWN:
                down = False
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
        
    pygame.display.update()
    fps.tick(60)