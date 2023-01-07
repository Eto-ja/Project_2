import pygame
import sys
import os
import pygame_gui

pygame.init()
pygame.display.set_caption('')
FPS = 120
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))
manager2 = pygame_gui.UIManager((800, 600))

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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Какая-то заставка хорошая", "",
                  "",
                  ""]

    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

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
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'key': load_image('key.png')
}

player_image = load_image('mar.png')

tile_width = tile_height = 50

tiles_group = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
keys_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            boxes_group.add(self)
        if tile_type == 'key':
            keys_group.add(self)

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

    # def update(self):
    #     if not pygame.sprite.collide_mask(self, self.mountain):
    #         self.rect = self.rect.move(0, 1)
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

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def start_game(player, camera):
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


def main():
    # start_screen()
    flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == close_button:
                    terminate()
                if event.ui_element == start_button:
                    player, _, _ = generate_level(load_level('1.txt'))
                    camera = Camera()
                    start_game(
                        player, camera
                    )
                if event.ui_element == record_button:
                    flag = True
                if event.ui_element == back_button:
                    flag = False
                if event.ui_element == button_1:
                    player, _, _ = generate_level(load_level('1.txt'))
                    camera = Camera()
                    start_game(player, camera)
                # if event.ui_element == button_2:
                #     player, _, _ = generate_level(load_level('map.txt'))
                #     camera = Camera()
                #     start_game(player, camera)

            manager2.process_events(event)
            manager.process_events(event)

        manager.update(FPS)
        manager2.update(FPS)
        screen.blit(background, (0, 0))
        if flag:
            manager2.draw_ui(screen)
        else:
            manager.draw_ui(screen)
        pygame.display.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    main()
