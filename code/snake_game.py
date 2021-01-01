import pygame
from pygame.locals import *
import time
import random

SIZE=25
window_x=800
window_y=600

class apple:
    def __init__(self,surface):
        self.surface = surface
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x=SIZE*3
        self.y=SIZE*3
        
    def draw(self):
        self.surface.blit(self.apple,(self.x,self.y))
        pygame.display.flip()
        
    def move(self):
        self.x=random.randint(1,window_x/SIZE-1)*SIZE
        self.y=random.randint(1,window_y/SIZE-1)*SIZE
        
class snake:
    def __init__(self,surface,length):
        self.surface=surface
        self.block=pygame.image.load("resources/block.jpg").convert()
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction="down"
        self.length=length
        
        
    def draw(self):
        
        for i in range(self.length):
            self.surface.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
        
    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
        
    def move_up(self):
        if self.direction!="down":
            self.direction='up'
        
    def move_down(self):
        if self.direction!="up":
            self.direction='down'
        
    def move_left(self):
        if self.direction!="right":
            self.direction='left'
        
    def move_right(self):
        if self.direction!="left":
            self.direction='right'
    
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
        
        
        if self.direction=="up":
            if self.y[0]-SIZE+1>0:
                self.y[0]-=SIZE
            else:
                self.y[0]=window_y-SIZE
                
        if self.direction=="down":
            if self.y[0]+SIZE-1<window_y-SIZE:
                self.y[0]+=SIZE
            else:
                self.y[0]=0
                
        if self.direction=="left":
            if self.x[0]-SIZE+1>0:
                self.x[0]-=SIZE
            else:
                self.x[0]=window_x-SIZE
                
        if self.direction=="right":
            if self.x[0]+SIZE-1<window_x-SIZE:
                self.x[0]+=SIZE
            else:
                self.x[0]=0
                
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_music()
        self.surface=pygame.display.set_mode((window_x,window_y))
        self.snake=snake(self.surface,1)
        self.snake.draw()
        self.apple=apple(self.surface)
        self.apple.draw()
        
    def render_background(self):
        bg=pygame.image.load("resources/backgroundjpg.jpg")
        self.surface.blit(bg,(0,0))
        
    def play_music(self):
        pygame.mixer.music.load("resources/background.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1,0)
        
    def play_sound(self,sound):
        sound=pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.set_volume(sound,0.1)
        pygame.mixer.Sound.play(sound)
        
    def easter(self):
        pygame.mixer.music.pause()
        font=pygame.font.SysFont('arial', 15)
        credit=font.render("you found the easter egg!!!!", True, (255, 255, 255))
        credit2=font.render("made by -> adeeb and dhaval patel(https://www.youtube.com/c/codebasics)", True, (255, 255, 255))
        credit3=font.render("game will resume in 5 seconds", True, (255, 255, 255))
        self.surface.blit(credit,(0,0))
        self.surface.blit(credit2,(0,16))
        self.surface.blit(credit3,(0,32))
        pygame.display.flip()
        time.sleep(5)
        pygame.mixer.music.unpause()
        return
        
    def reset(self):
        self.snake = snake(self.surface,1)
        self.apple = apple(self.surface)
        
    def show_score(self,length):
        font=pygame.font.SysFont('arial',30)
        score=font.render(f'score: {length}',True,(255,255,255))
        self.surface.blit(score,(450,25))
    
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.show_score(self.snake.length)
        pygame.display.flip()
                
        #collision with apple
        if self.iscollision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("apple")
            self.apple.move()
            self.snake.increase_length()
                
        #collision with egg
        if self.iscollision(self.snake.x[0], self.snake.y[0], 450, 25):
            self.play_sound("egg")
            self.easter()
                
        #collision with self
        for i in range(3,self.snake.length):
            if self.iscollision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                pygame.mixer.music.pause()
                self.play_sound("game_over")
                raise "game over"
                
    def iscollision(self,x1,y1,x2,y2):
        if y1>=y2 and y1<y2+SIZE:
            if x1>=x2 and x1<x2+SIZE:
                return True
        return False
    
    def is_collision(self,x1,y1,x2,y2):
        if x1 == x2 and y1 == y2:
            return True
        return False
    
    def run(self):
        pause=False
        running=True
        while running:#event loop
            for event in pygame.event.get():
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                            running = False
                            
                    if event.key == K_RETURN:
                        pygame.mixer.music.play(-1,0)
                        pause=False
                        
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                            
                        if event.key == K_DOWN:
                            self.snake.move_down()
                            
                        if event.key == K_LEFT:
                            self.snake.move_left()
                            
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                            
                if event.type == QUIT:
                    running = False
            try:
                if not pause:
                    game.play()
            
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(.2)

if __name__=="__main__":
    game=Game()
    game.run()
    
    pygame.quit()