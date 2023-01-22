import pygame
import sys
import os
import pygame_gui
import datetime

pygame.init()
pygame.display.set_caption('')
FPS = 120
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')
manager2 = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')
manager3 = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')

# создание кнопок
close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 40, HEIGHT // 2), (120, 50)),
                                            text='Выйти',
                                            manager=manager)
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 40, HEIGHT // 2 - 150), (120, 50)),
                                            text='Начать',
                                            manager=manager)
how_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 40, HEIGHT // 2 - 100), (120, 50)),
                                          text='Как играть',
                                          manager=manager)
record_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 40, HEIGHT // 2 - 50), (120, 50)),
                                             text='Уровни',
                                             manager=manager)
button_1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 70), (50, 50)),
                                        text='1',
                                        manager=manager2)
button_2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((80, 70), (50, 50)),
                                        text='2',
                                        manager=manager2)
back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH - 110, 10), (100, 50)),
                                           text='Назад',
                                           manager=manager2)
next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 200), (170, 50)),
                                           text='Следующий уровень',
                                           manager=manager3)
menu_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((190, 280), (140, 50)),
                                           text='Меню',
                                           manager=manager3)
zanavo_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((340, 200), (150, 50)),
                                             text='Пройти заново',
                                             manager=manager3)


# закрытие программы
def terminate():
    pygame.quit()
    sys.exit()


# отрисовка текста
def text(font, intro_text, color):
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


# правила игры
def how():
    intro_text = ["Правила игры", "",
                  "Каждый уровень представляет собой лабиринт,",
                  "нужно найти ключ, затем выйти через дверь.",
                  "Без ключа выйти через дверь не получиться"]

    font_2 = pygame.font.SysFont('Arial', 25)
    pygame.draw.rect(
        screen, pygame.Color('grey'), (380, 50, 80, 30))
    text(font_2, intro_text, 'blue')
    screen.blit(font_2.render('Назад', True, pygame.Color('black')), (380, 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# загрузка уровня
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    if not os.path.isfile(filename):
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


all_sprites = pygame.sprite.Group()


# здесь происходит анимация во время передвижения персонажа
# w1 и w2 - передаются кол-во персонажей, k - кол-во кадров, name - имя файла, position - позиция,
# p - в какую сторону движение
def my_animation(w1, h1, k, fps, name, position, p):
    animation_frames = []
    timer = pygame.time.Clock()

    sprite = pygame.image.load("data/{0}.png".format(name)).convert_alpha()

    width, height = sprite.get_size()
    w, h = width / w1, height / h1

    row = 0

    for j in range(int(height / h)):
        for i in range(int(width / w)):
            animation_frames.append(sprite.subsurface(pygame.Rect(i * w, row, w, h)).convert_alpha())
        row += int(h)

    counter = 0
    q = 0

    while q < 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(animation_frames[counter], position)

        # движение вправо
        if p == 1:
            position = position[0] + 25, position[1]
        # движение влево
        if p == 2:
            position = position[0] - 25, position[1]
        # движение вниз
        if p == 3:
            position = position[0], position[1] + 25
        # движение вверх
        if p == 4:
            position = position[0], position[1] - 25

        counter = (counter + 1) % k
        q += 1

        pygame.display.update()
        timer.tick(fps)


tile_images = {
    'wall': load_image('kust.png'),
    'empty': load_image('linilium.png'),
    'key': load_image('key-transformed.png'),
    'door_close': load_image('door_close.png')
}

player_image = load_image("people_stop-transformed.png").convert_alpha()

tile_width = tile_height = 50

tiles_group = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
keys_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()

start_time = 0
shrift = False
flag_end = False
file = ['map.txt', '1.txt']
number = 1
flag = False
stop = False
stop_2 = False
button = 0


# рисуется карта
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            boxes_group.add(self)
        if tile_type == 'key':
            keys_group.add(self)
        if tile_type == 'door_close':
            door_group.add(self)

        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# рисуется персонаж
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.keys = 0
        self.play = False

    def right(self):
        self.rect.x += 5
        if self.check_collide():
            self.rect.x -= 5
        else:
            self.rect.x -= 5
            my_animation(5, 1, 5, 15, "people_left-transformed", (self.rect.x, self.rect.y), 1)
            self.rect.x += 50

    def left(self):
        self.rect.x -= 5
        if self.check_collide():
            self.rect.x += 5
        else:
            self.rect.x += 5
            my_animation(5, 1, 5, 15, "people_right-transformed", (self.rect.x, self.rect.y), 2)
            self.rect.x -= 50

    def down(self):
        self.rect.y += 5
        if self.check_collide():
            self.rect.y -= 5
        else:
            self.rect.y -= 5
            my_animation(5, 1, 5, 15, "people_down-transformed", (self.rect.x, self.rect.y), 3)
            self.rect.y += 50

    def up(self):
        self.rect.y -= 5
        if self.check_collide():
            self.rect.y += 5
        else:
            self.rect.y += 5
            my_animation(5, 1, 5, 15, "people_up-transformed", (self.rect.x, self.rect.y), 4)
            self.rect.y -= 50

    # чтобы персонаж не ходил сквозь стены
    def check_collide(self):
        if pygame.sprite.spritecollide(self, boxes_group, False):
            return True
        return False

    # проверка на столкновение с ключами или дверью
    def update(self):
        global stop, stop_2
        key = pygame.sprite.spritecollide(self, keys_group, False)
        if len(key) != 0:
            key = key[0]
            self.keys += 1
            key.kill()

        door = pygame.sprite.spritecollide(self, door_group, False)
        if len(door) != 0:
            if self.keys == 1:
                stop_2 = True


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.width = 500
        self.height = 500

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Tile('empty', x, y)
                Tile('key', x, y)
            elif level[y][x] == ';':
                Tile('door_close', x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


# очищение всех групп перед новой игрой
def clear():
    global shrift, all_sprites, boxes_group, door_group, keys_group, tiles_group
    shrift = False
    all_sprites = pygame.sprite.Group()
    boxes_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    keys_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()


def start_game(player, camera):
    global start_time, stop, number, all_sprites, boxes_group, door_group, keys_group, tiles_group, button, shrift, \
        flag_end, flag, stop_2
    shrift = False
    start_time = datetime.datetime.now()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    player.right()
                if keys[pygame.K_LEFT]:
                    player.left()
                if keys[pygame.K_DOWN]:
                    player.down()
                if keys[pygame.K_UP]:
                    player.up()

        clock.tick(FPS)
        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)

        camera.update(player)

        for sprite in all_sprites:
            camera.apply(sprite)

        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        # если игра закончилась
        if stop:
            button = 0
            end(start_time)
            screen.fill((0, 0, 0))
            stop = False
            start_time = datetime.datetime.now()
            clear()
            # если нажали кнопку следующая игра
            if button == 1:
                player_group.remove(player)
                if number == 2:
                    flag = False
                    return
                else:
                    number += 1
                    player, _, _ = generate_level(load_level(file[number - 1]))
                    player_group.add(player)
                    all_sprites.add(player)
                    camera = Camera()
            # если нажали кнопку меню
            if button == 2:
                flag_end = False
                flag = False
                return
            # если нажали кнопку пройти заново
            if button == 3:
                player_group.remove(player)
                player, _, _ = generate_level(load_level(file[number - 1]))
                player_group.add(player)
                all_sprites.add(player)
        if stop_2:
            stop = True


# класс финального окна
class Game(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = load_image(filename)
        self.rect = self.image.get_rect()
        self.flag = True
        self.rect.y -= 600

    def move(self):
        global shrift
        if self.rect.y < 0:
            self.rect.y += 1
        if self.rect.y == 0:
            shrift = True


# конец игры
def end(start_time):
    global flag_end, number, file, stop, button, shrift, flag, stop_2
    delta = datetime.datetime.now() - start_time
    game = Game('green.png')
    fps = 600
    clock = pygame.time.Clock()
    intro_text = [f"Уровень {number} пройден", "",
                  f"Потраченное время: {delta.seconds} секунд(ы)",
                  ""]

    # опускается зелёный экран
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == next_button:
                    button = 1
                    flag_end = False
                    return
                if event.ui_element == menu_button:
                    flag_end = False
                    flag = False
                    button = 2
                    return
                if event.ui_element == zanavo_button:
                    button = 3
                    flag_end = False
                    return
            manager3.process_events(event)
        game.move()
        screen.blit(game.image, game.rect)
        clock.tick(fps)
        if shrift:
            font = pygame.font.Font(None, 30)
            text(font, intro_text, 'black')
            flag_end = True
        if flag_end:
            manager3.update(FPS)
            manager3.draw_ui(screen)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)
        stop = False
        stop_2 = False


# основной цикл, проверяет кнопки меню и уровней
def main():
    global file, number, flag_end, flag, number
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == close_button:
                    terminate()
                if event.ui_element == start_button:
                    player, _, _ = generate_level(load_level(file[number - 1]))
                    camera = Camera()
                    start_game(
                        player, camera
                    )
                if event.ui_element == record_button:
                    flag = True
                if event.ui_element == back_button:
                    flag = False
                if event.ui_element == button_1:
                    number = 1
                    player, _, _ = generate_level(load_level(file[0]))
                    camera = Camera()
                    start_game(player, camera)
                if event.ui_element == button_2:
                    number = 2
                    player, _, _ = generate_level(load_level(file[1]))
                    camera = Camera()
                    start_game(player, camera)
                if event.ui_element == next_button:
                    flag_end = False
                    player, _, _ = generate_level(load_level(file[number - 1]))
                    camera = Camera()
                    start_game(player, camera)
                if event.ui_element == menu_button:
                    flag_end = False
                    flag = False
                if event.ui_element == zanavo_button:
                    flag_end = False
                    player, _, _ = generate_level(load_level(file[number - 1]))
                    camera = Camera()
                    start_game(player, camera)
                if event.ui_element == how_button:
                    screen.fill((0, 0, 0))
                    how()

            manager2.process_events(event)
            manager.process_events(event)
            manager3.process_events(event)

        screen.blit(background, (0, 0))
        manager2.update(FPS)
        manager.update(FPS)
        manager3.update(FPS)
        if flag:
            manager2.draw_ui(screen)
        else:
            manager.draw_ui(screen)
        if flag_end:
            manager3.draw_ui(screen)
        pygame.display.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    main()
