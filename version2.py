import pygame,sys,time,random
from pygame.locals import *

redColour = pygame.Color(255,0,0)
blackColour = pygame.Color(0,0,0)
greyColour = pygame.Color(0,0,255)
deff=5

def gameOver(playSurface,point):
    gameOverFont = pygame.font.SysFont('Arial',30,True)
    gameOverSurf = gameOverFont.render('game over',True, redColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 10)
    playSurface.blit(gameOverSurf, gameOverRect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()
def main():
    point=0
    deff=5
    pygame.mixer.init()
    pygame.mixer.music.load('bg.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)
    a=random.randrange(0,255)
    b=random.randrange(0,255)
    c=random.randrange(0,255)
    whiteColour = pygame.Color(a,b,c)
    pygame.init()
    fpsClock = pygame.time.Clock()
    
    playSurface = pygame.display.set_mode((600,600))
    pygame.display.set_caption('Raspberry Snake')

    
    snakePosition = [100,100]
    snakeSegments = [[100,100],[80,100],[60,100]]
    raspberryPosition = [300,300]
    raspberry1Position = [280,100]
    raspberry2Position = [80,80]
    raspberrySpawned = 3
    direction = 'right'
    changeDirection = direction

    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                
                if event.key == K_RIGHT or event.key == ord('d'):
                    changeDirection = 'right'
                if event.key == K_LEFT or event.key == ord('a'):
                    changeDirection = 'left'
                if event.key == K_UP or event.key == ord('w'):
                    changeDirection = 'up'
                if event.key == K_DOWN or event.key == ord('s'):
                    changeDirection = 'down'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
       
        if changeDirection == 'right' and not direction == 'left':
            direction = changeDirection
        if changeDirection == 'left' and not direction == 'right':
            direction = changeDirection
        if changeDirection == 'up' and not direction == 'down':
            direction = changeDirection
        if changeDirection == 'down' and not direction == 'up':
            direction = changeDirection
       
        if direction == 'right':
            snakePosition[0] += 20
        if direction == 'left':
            snakePosition[0] -= 20
        if direction == 'up':
            snakePosition[1] -= 20
        if direction == 'down':
            snakePosition[1] += 20
        pygame.display.flip()
        
        snakeSegments.insert(0,list(snakePosition))
        deff+=0.5
        point+=1
        
        if snakePosition[0] == raspberryPosition[0] and snakePosition[1] == raspberryPosition[1]:
            raspberrySpawned = 0
            
        elif snakePosition[0] == raspberry1Position[0] and snakePosition[1] == raspberry1Position[1]:
            raspberrySpawned = 1
            
        elif snakePosition[0] == raspberry2Position[0] and snakePosition[1] == raspberry2Position[1]:
            raspberrySpawned = 2
            
        else:
            snakeSegments.pop()
            deff-=0.5
            point-=1
        
        if raspberrySpawned == 0 :
            x = random.randrange(1,30)
            y = random.randrange(1,22)
            raspberryPosition = [int(x*20),int(y*20)]
            raspberrySpawned =3
        if raspberrySpawned == 1 :
            x = random.randrange(1,30)
            y = random.randrange(1,22)
            raspberry1Position = [int(x*20),int(y*20)]
            raspberrySpawned =3
        if raspberrySpawned == 2 :
            x = random.randrange(1,30)
            y = random.randrange(1,22)
            raspberry2Position = [int(x*20),int(y*20)]
            raspberrySpawned =3
        
        playSurface.fill(blackColour)
        a=random.randrange(0,255)
        b=random.randrange(0,255)
        c=random.randrange(0,255)
        whiteColour = pygame.Color(a,b,c)
        for position in snakeSegments:
            pygame.draw.rect(playSurface,greyColour,Rect(position[0],position[1],20,20))
            
            
            '''
            a=random.randrange(0,255)
            b=random.randrange(0,255)
            c=random.randrange(0,255)
            whiteColour = pygame.Color(a,b,c)
            '''

        pygame.draw.rect(playSurface,whiteColour,Rect(snakePosition[0],snakePosition[1],20,20))
        
        pygame.draw.rect(playSurface,redColour,Rect(raspberryPosition[0], raspberryPosition[1],20,20))
        pygame.draw.rect(playSurface,redColour,Rect(raspberry1Position[0], raspberry1Position[1],20,20))
        pygame.draw.rect(playSurface,redColour,Rect(raspberry2Position[0], raspberry2Position[1],20,20))
        
        pygame.display.flip()
        
        
        if snakePosition[0] > 600 or snakePosition[0] < 0:
            gameOver(playSurface,point)
        if snakePosition[1] > 600 or snakePosition[1] < 0:
            gameOver(playSurface,point)
        if snakePosition in snakeSegments[1:] :
            gameOver(playSurface,point)
       
        fpsClock.tick(deff)
        pygame.display.flip()
if __name__ == "__main__":
    main()
