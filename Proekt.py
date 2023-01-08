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

manager = pygame_gui.UIManager((WIDTH, HEIGHT))
manager2 = pygame_gui.UIManager((WIDTH, HEIGHT))
manager3 = pygame_gui.UIManager((WIDTH, HEIGHT))

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


def terminate():
    pygame.quit()
    sys.exit()


def how():
    intro_text = ["Правила игры", "",
                  "Каждый уровень представляет собой лабиринт,",
                  "нужно найти ключ, затем выйти через дверь.",
                  "Без ключа выйти через дверь не получиться"]

    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    font_2 = pygame.font.SysFont('Arial', 25)
    pygame.draw.rect(
        screen, pygame.Color('grey'), (380, 50, 80, 30))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font_2.render(line, 1, pygame.Color('blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
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


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


tile_images = {
    'wall': load_image('kust.png'),
    'empty': load_image('linilium.png'),
    'key': load_image('key.png'),
    'door_open': load_image('door_open.png'),
    'door_close': load_image('door_close.png')
}

player_image = load_image('mar.png')

tile_width = tile_height = 50

tiles_group = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
keys_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()

start_time = 0
shrift = False
flag_end = False
file = ['1.txt', 'map.txt']
number = 1
flag = False


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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.keys = 0

    def right(self):
        self.rect.x += 50
        if self.check_collide():
            self.left()

    def left(self):
        self.rect.x -= 50
        if self.check_collide():
            self.right()

    def down(self):
        self.rect.y += 50
        if self.check_collide():
            self.up()

    def up(self):
        self.rect.y -= 50
        if self.check_collide():
            self.down()

    def check_collide(self):
        if pygame.sprite.spritecollide(self, boxes_group, False):
            return True
        return False

    def update(self):
        key = pygame.sprite.spritecollide(self, keys_group, False)
        if len(key) != 0:
            key = key[0]
            self.keys += 1
            keys_group.remove(key)
            all_sprites.remove(key)
            tiles_group.remove(key)
        door = pygame.sprite.spritecollide(self, door_group, False)
        if len(door) != 0:
            if self.keys == 1:
                end(start_time)


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


def start_game(player, camera):
    global start_time
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


def end(start_time):
    global flag_end, number, file
    delta = datetime.datetime.now() - start_time
    game = Game('green.png')
    fps = 300
    clock = pygame.time.Clock()
    intro_text = [f"Уровень {number} пройден", "",
                  f"Потраченное время: {delta.seconds} секунд",
                  ""]

    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    if len(file) < number:
        number += 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        game.move()
        screen.blit(game.image, game.rect)
        clock.tick(fps)
        if shrift:
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            flag_end = True
        if flag_end:
            # end_2()
            manager3.update(FPS)
            manager3.draw_ui(screen)
        pygame.display.update()
        pygame.display.flip()


# def end_2():
    # global file, number, flag_end, flag
    # # while True:
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         sys.exit()
    #     if event.type == pygame_gui.UI_BUTTON_PRESSED:
    #         if event.ui_element == next_button:
    #             print('nexrt')
    #             flag_end = False
    #             player, _, _ = generate_level(load_level(file[number - 1]))
    #             camera = Camera()
    #             start_game(player, camera)
    #         if event.ui_element == menu_button:
    #             print('menu')
    #             flag_end = False
    #             flag = False
    #         if event.ui_element == zanavo_button:
    #             print('zanovo')
    #             flag_end = False
    #             player, _, _ = generate_level(load_level(file[number - 1]))
    #             camera = Camera()
    #             start_game(player, camera)
    #
    #     manager2.process_events(event)
    #     manager.process_events(event)
    #     manager3.process_events(event)
    #
    #     screen.blit(background, (0, 0))
    #     manager2.update(FPS)
    #     manager.update(FPS)
    #     manager3.update(FPS)
    #     if flag:
    #         manager2.draw_ui(screen)
    #     else:
    #         manager.draw_ui(screen)
    #     if flag_end:
    #         manager3.draw_ui(screen)
    #     pygame.display.update()
    #     # all_sprites.draw(screen)
    #     pygame.display.flip()
    #     clock.tick(FPS)


def main():
    global file, number, flag_end, flag
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == close_button:
                    print('close')
                    terminate()
                if event.ui_element == start_button:
                    print('start')
                    player, _, _ = generate_level(load_level(file[number - 1]))
                    camera = Camera()
                    start_game(
                        player, camera
                    )
                if event.ui_element == record_button:
                    print('record')
                    flag = True
                if event.ui_element == back_button:
                    print('back')
                    flag = False
                if event.ui_element == button_1:
                    print('1')
                    number = 1
                    player, _, _ = generate_level(load_level(file[0]))
                    camera = Camera()
                    start_game(player, camera)
                if event.ui_element == button_2:
                    print('2')
                    number = 2
                    player, _, _ = generate_level(load_level(file[1]))
                    camera = Camera()
                    start_game(player, camera)
                if event.ui_element == next_button:
                    print('nexrt')
                    flag_end = False
                    player, _, _ = generate_level(load_level(file[number - 1]))
                    camera = Camera()
                    start_game(player, camera)
                if event.ui_element == menu_button:
                    print('menu')
                    flag_end = False
                    flag = False
                if event.ui_element == zanavo_button:
                    print('zanovo')
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
