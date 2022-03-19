import pygame
import const
import numpy as np

window = pygame.display.set_mode((const.WINDOW_RESOLUTION,const.WINDOW_RESOLUTION))
pygame.display.set_caption("Maze Solver")
grid = np.zeros((const.TILE_NB,const.TILE_NB))
start = (None,None)
end = (None,None)

def draw_window(window, grid):
    window.fill(const.BACKGROUND_COLOR)
    drawGrid(window, grid)

    pygame.display.update()

def drawGrid(window, grid):
    global start, end
    blockSize = const.WINDOW_RESOLUTION/const.TILE_NB
    for x in range(len(grid)):
        row = grid[x]
        for y in range(len(row)):
            tile = row[y]
            rect = pygame.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            if tile == 0:
                color = const.BACKGROUND_COLOR
                if start == (x,y):
                    color = const.START_COLOR
                elif end == (x,y):
                    color = const.END_COLOR
                pygame.draw.rect(window, color, rect, 0)
            if tile == 1:
                pygame.draw.rect(window, const.WALL_COLOR, rect, 0)

            # Borders
            pygame.draw.rect(window, const.WALL_COLOR, rect, 1)
            

def get_tile_index(x,y):
    blockSize = const.WINDOW_RESOLUTION/const.TILE_NB
    return int(x/blockSize), int(y/blockSize)


def main():
    global window, grid, start, end

    clock = pygame.time.Clock()
    run = True
    while run:
        if (const.FPS != -1):
            clock.tick(const.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        x, y = get_tile_index(x,y)
        if mouse_pressed[0]:
            # Left click            
            grid[x][y] = 1
            if start == (x,y): start = (None,None)
            if end == (x,y): end = (None,None)
        if mouse_pressed[2]:
            # Right click 
            if start == (x,y): start = (None,None)
            if end == (x,y): end = (None,None)        
            grid[x][y] = 0
        if key_pressed[pygame.K_s]:
            grid[x][y]
            start = (x,y)
        if key_pressed[pygame.K_f]:
            grid[x][y]
            end = (x,y)
            

        draw_window(window, grid)
        
        

    pygame.quit()

if __name__ == "__main__":
    main()