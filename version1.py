from random import randint
from abc import ABCMeta, abstractmethod
import pygame 

BLACK_COLOR = [0, 0, 0]
FOOD_COLOR = [100, 202, 80]
GREEN_COLOR = [48, 172, 80]
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class GameObject(object, metaclass=ABCMeta):
    def __init__(self, x, y, color):
        self._x = x
        self._y = y
        self._color = color

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @abstractmethod
    def draw(self, screen):
        pass


class Food(GameObject):
    def __init__(self, x, y, size, color=FOOD_COLOR):
        super(Food, self).__init__(x, y, color)
        self._size = size
        self._hidden = False

    def draw(self, screen):
        if not self._hidden:
            pygame.draw.circle(screen, self._color,
                               (self._x + self._size // 2, self._y + self._size // 2)
                               , self._size // 2, 0)
        self._hidden = not self._hidden


class Wall(GameObject):
    def __init__(self, x, y, width, height, color=BLACK_COLOR):
        super(Wall, self).__init__(x, y, color)
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def draw(self,screen):
        pygame.draw.rect(screen, self._color,
                        (self._x,self._y,self._width,self._height), 4)


class SnakeNode(GameObject):
    def __init__(self, x, y, size, color =GREEN_COLOR):
        super(SnakeNode, self).__init__(x, y, color)
        self._size = size

    @property
    def size(self):
        return  self._size

    def draw(self, screen):
        pygame.draw.rect(screen, self._color,
                         (self._x, self._y, self._size, self._size), 0)
        pygame.draw.rect(screen, BLACK_COLOR,
                         (self._x, self._y, self._size, self._size), 1)


class Snake(GameObject):
    def __init__(self):
        super(Snake, self).__init__(290, 250, GREEN_COLOR)
        self._dir = LEFT
        self._nodes = []
        self._eat_food = False
        for index in range(5):
            node = SnakeNode(self._x + index * 20, self._y, 20)
            self._nodes.append(node)

    @property
    def dir(self):
        return self._dir

    @property
    def head(self):
        return self._nodes[0]

    def draw(self, screen):
        for node in self._nodes:
            node.draw(screen)

    def move(self):
        head = self.head
        snake_dir = self._dir
        x, y, size = head.x, head.y, head.size
        if snake_dir == UP:
            y -= size
        elif snake_dir == RIGHT:
            x += size
        elif snake_dir == DOWN:
            y += size
        elif snake_dir == LEFT:
            x -= size
        new_head = SnakeNode(x, y, size)
        self._nodes.insert(0,new_head)
        if self._eat_food:
            self._eat_food = False
        else:
            self._nodes.pop()   # pop() 默认删掉最后一位

    def change_dir(self,new_dir):
        if (self._dir + new_dir) % 2 != 0:
            self._dir = new_dir

    def collide(self, wall):
        """
    撞墙
        :param wall: 围墙
        :return: 蛇撞到墙返回True,否则返回False
        """
        head = self.head
        return head.x < wall.x or head.x + head.size > wall.x + wall.width \
        or head.y < wall.y or head.y + head.size > wall.y + wall.height



    def eat_food(self,food):
        if self.head.x == food.x and self.head.y == food.y:
            self._eat_food = True
            return True
        return False

    def eat_me(self):
        head = self.head
        for i in range(4,len(self._nodes)):
            if head.x == self._nodes[i].x and head.y == self._nodes[i].y:
                return True




def main():
    def refresh():
        """刷新游戏窗口"""
        screen.fill([255, 255, 255])
        wall.draw(screen)
        food.draw(screen)
        snake.draw(screen)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(str(score), False, GREEN_COLOR)
        text1 = font.render('GAME OVER',False,[255,0,0])
        t = text.get_rect()
        t1 = text.get_rect()
        t.center = (400, 50)
        t1.center = (400,400)
        screen.blit(text, t)
        pygame.display.flip()


    def handle_key_event(key_event):
        """处理按键事件"""
        key = key_event.key
        if key == pygame.K_w:
            new_dir = UP
        elif key == pygame.K_d:
            new_dir = RIGHT
        elif key == pygame.K_s:
            new_dir = DOWN
        elif key == pygame.K_a:
            new_dir = LEFT
        elif key == pygame.K_r:
            reset_game()
            return
        else:
            return
        if new_dir != snake.dir:
            snake.change_dir(new_dir)

    def create_food():
        row = randint(0,35)
        col = randint(0,35)
        return Food(10 + 20 * col, 10 + 20 * row, 20)

    def reset_game():
        nonlocal food, snake, game_over
        game_over = False
        food = create_food()
        snake = Snake()
        pygame.event.clear()



    wall = Wall(10, 10, 780, 780)
    food = create_food()
    snake = Snake()
    pygame.init()


    score = 0
    screen = pygame.display.set_mode([800,800])
    pygame.display.set_caption('贪吃蛇')
    screen.fill([255,255,255])

    pygame.display.flip()
    clock= pygame.time.Clock()
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_key_event(event)
        if not game_over:
            refresh()

        clock.tick(15)
        if not game_over:
            snake.move()
            if snake.eat_food(food):
                food = create_food()
                score += 1
        if snake.collide(wall):
            game_over = True
        if snake.eat_me():
            game_over = True
        font = pygame.font.Font('freesansbold.ttf', 32)
        text1 = font.render('GAME OVER', False, [255, 125, 96])
        t1 = text1.get_rect()
        t1.center = (400, 400)
        pygame.display.flip()
        if game_over:
            screen.blit(text1, t1)



    pygame.quit()


if __name__ == '__main__':
    main()
@abstractmethod
def draw(self, screen):
   pass

