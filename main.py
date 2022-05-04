from cgitb import reset
import time
import pygame
import random

SIZE = 15
BACKGROUND_COLOR = (0, 0, 0)
COLOR = (255, 255, 255)

class Apple:
    def __init__(self, screen):
        
        self.screen = screen

        self.color = COLOR
        self.x = 300
        self.y = 300

    def draw(self):
        self.block = pygame.Rect(self.x, self.y, SIZE, SIZE)
        pygame.draw.rect(self.screen, self.color, self.block)  
        pygame.display.flip()

    def move_apple(self):
        self.x = random.randint(0, 39)*SIZE
        self.y = random.randint(0, 39)*SIZE
            

class Snake:
    def __init__(self, screen, length):
        
        self.screen = screen
        self.length = length


        self.color = COLOR
        self.x = [SIZE]*self.length
        self.y = [SIZE]*self.length
        self.direction = "right"

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        for i in range(self.length):
            self.block = pygame.Rect(self.x[i], self.y[i], SIZE, SIZE)      
            pygame.draw.rect(self.screen, self.color, self.block)
        
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])
        

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE
        elif self.direction == "right":
            self.x[0] += SIZE
        elif self.direction == "down":
            self.y[0] += SIZE
        elif self.direction == "left":
            self.x[0] -= SIZE
        
        self.draw()


    def move_up(self):
        self.direction = "up"

    def move_right(self):
        self.direction = "right"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

class Game:
    def __init__(self):
        pygame.init()
                
        self.screen = pygame.display.set_mode((600, 600))
        self.screen.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.screen, 3)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()

    def is_collision(self, toCollision_x, toCollision_y):
        if self.snake.x[0] == toCollision_x and self.snake.y[0] == toCollision_y: 
            return True

    def display_score(self):
        font = pygame.font.SysFont("arial", 20)
        score = font.render(f"Score: {self.snake.length - 3}", True, COLOR)
        self.screen.blit(score, (500, 10))

    def play(self):

        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        

        # Collison with apple
        if self.is_collision(self.apple.x, self.apple.y):
            self.apple.move_apple()
            self.snake.increase_length()

        # Colllision with itself.
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i]):
                raise "GAME OVER"

    def show_game_over(self):
        self.screen.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont("arial", 20)
        game_over_l1 = font.render(f"Game is over! Your score is {self.snake.length - 3}", True, COLOR)
        self.screen.blit(game_over_l1, (75, 200))
        game_over_l2 = font.render("To play again press Enter. To exit press Escape", True, COLOR)
        self.screen.blit(game_over_l2, (75, 250))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.screen, 3)
        self.apple = Apple(self.screen)

    def run(self):
        running = True
        pause = False

        while running:
                        
            for event in pygame.event.get():    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        pause = False
                    elif event.key == pygame.K_UP and self.snake.direction != "down":
                        self.snake.move_up()
                    elif event.key == pygame.K_RIGHT and self.snake.direction != "left":
                        self.snake.move_right()
                    elif event.key == pygame.K_DOWN and self.snake.direction != "up":
                        self.snake.move_down()    
                    elif event.key == pygame.K_LEFT and self.snake.direction != "right":
                        self.snake.move_left()
                elif event.type == pygame.QUIT:
                    running = False

            try: 
                if not pause:
                    self.play()    
                    time.sleep(0.1)

            except Exception as e:
                pause = True
                self.show_game_over()
                self.reset()


if __name__ == "__main__":

    game = Game()
    game.run()
