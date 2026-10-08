#pgzero
from pgzero.builtins import *  # <--- Добавь эту строку в самую первую строчку!
import random, pygame, pgzrun

# Игровое окно
cell = Actor('border')
cell1 = Actor('floor')
cell2 = Actor("crack")
cell3 = Actor("bones")
size_w = 9 # Ширина поля в клетках
size_h = 10 # Высота поля в клетках
WIDTH = cell.width * size_w
HEIGHT = cell.height * size_h

win = 0
mode = "game"

TITLE = "WeCode и Драконы" # Заголовок окна игры
FPS = 30 # Количество кадров в секунду
my_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 1, 1, 2, 1, 3, 1, 1, 0], 
          [0, 1, 1, 1, 2, 1, 1, 1, 0], 
          [0, 1, 3, 2, 1, 1, 3, 1, 0], 
          [0, 1, 1, 1, 1, 3, 1, 1, 0], 
          [0, 1, 1, 3, 1, 1, 2, 1, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [-1, -1, -1, -1, -1, -1, -1, -1, -1]] # Строка с атакой и здоровьем

# Главный герой
char = Actor('stand')
char.top = cell.height
char.left = cell.width
char.health = 100
char.attack = 5

# Функция для генерации врагов
def create_enemies():
    new_enemies = []
    for i in range(5):
        x = random.randint(1, 7) * cell.width
        y = random.randint(1, 7) * cell.height
        enemy = Actor("enemy", topleft = (x, y))
        enemy.health = random.randint(10, 20)
        enemy.attack = random.randint(5, 10)
        enemy.bonus = random.randint(0, 2)
        new_enemies.append(enemy)
    return new_enemies

# Генерация врагов
enemies = create_enemies()

# Бонусы
hearts = []
swords = []   

# Отрисовка карты
def map_draw():
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                cell.left = cell.width*j
                cell.top = cell.height*i
                cell.draw()
            elif my_map[i][j] == 1:
                cell1.left = cell.width*j
                cell1.top = cell.height*i
                cell1.draw()
            elif my_map[i][j] == 2:
                cell2.left = cell.width*j
                cell2.top = cell.height*i
                cell2.draw()  
            elif my_map[i][j] == 3:
                cell3.left = cell.width*j
                cell3.top = cell.height*i
                cell3.draw() 

# Отрисовка
def draw():
    if mode == 'game' or mode == 'level_2':
        screen.fill("#2f3542")
        map_draw()
        char.draw()
        screen.draw.text("HP:", center=(25, 475), color = 'white', fontsize = 20)
        screen.draw.text(str(char.health), center=(75, 475), color = 'white', fontsize = 20)
        screen.draw.text("AP:", center=(375, 475), color = 'white', fontsize = 20)
        screen.draw.text(str(char.attack), center=(425, 475), color = 'white', fontsize = 20)
        for i in range(len(enemies)):
            enemies[i].draw()
            screen.draw.text(str(enemies[i].health), center=(enemies[i].x-5, enemies[i].y-35), color = 'red', fontsize = 20)
            screen.draw.text(str(enemies[i].attack), center=(enemies[i].x-5, enemies[i].y+35), color = 'black', fontsize = 20)
        # отрисовка бонусов
        for i in range(len(hearts)):
            hearts[i].draw()
        for i in range(len(swords)):
            swords[i].draw()
        
    # Окно победы или поражения    
    elif mode == "end":
        if win == 2:
            screen.fill("#1e3799")
            screen.draw.text("ПОБЕДА!", center=(WIDTH / 2, HEIGHT / 2 - 40), color = "yellow", fontsize = 52)
            screen.draw.text("Все монстры побеждены!", center=(WIDTH / 2, HEIGHT / 2 + 10), color = "white", fontsize = 22)
        else:
            screen.fill("#b22222")
            screen.draw.text("ПОРАЖЕНИЕ!", center=(WIDTH / 2, HEIGHT / 2 - 40), color = "black", fontsize = 52)
            screen.draw.text("Герой пал в бою...", center=(WIDTH / 2, HEIGHT / 2 + 10), color = "white", fontsize = 22)
            
        screen.draw.text("Нажмите ENTER, чтобы играть снова", center=(WIDTH / 2, HEIGHT / 2 + 70), color = "yellow", fontsize = 20)


# Управление
def on_key_down(key, *args):
    global mode, win, enemies, hearts, swords

    # Перезапуск игры
    if mode == "end":
        if key == keys.RETURN or key == keys.KP_ENTER:
            char.health = 100
            char.attack = 5
            char.top = cell.height
            char.left = cell.width
            char.image = 'stand'
            enemies = create_enemies()
            hearts = []
            swords = []
            win = 0
            mode = "game"
        return

    # Передвижение персонажа
    if mode == "game":
        old_x = char.x
        old_y = char.y
        if (key == keys.RIGHT or keyboard.right) and char.x + cell.width < WIDTH - cell.width:
            char.x += cell.width
            char.image = 'stand'
        elif (key == keys.LEFT or keyboard.left) and char.x - cell.width > cell.width:
            char.x -= cell.width
            char.image = 'left'
        elif (key == keys.DOWN or keyboard.down) and char.y + cell.height < HEIGHT - cell.height*2:
            char.y += cell.height
        elif (key == keys.UP or keyboard.up) and char.y - cell.height > cell.height:
            char.y -= cell.height
            
        # Столкновение с врагами
        enemy_index = char.collidelist(enemies)
        if enemy_index != -1:
            char.x = old_x
            char.y = old_y
            enemy = enemies[enemy_index]
            enemy.health -= char.attack
            char.health -= enemy.attack
            if enemy.health <= 0:
                # Добавление бонусов
                if enemy.bonus == 1:
                    heart = Actor('heart')
                    heart.pos = enemy.pos
                    hearts.append(heart)
                elif enemy.bonus == 2:
                    sword = Actor('sword')
                    sword.pos = enemy.pos
                    swords.append(sword)
                enemies.pop(enemy_index)

# Логика победы или поражения
def victory():
    global mode, win
    if enemies == [] and char.health > 0:
        mode == "level_2"
        win += 1
        char.health += 100
        for i in range(5):
            x = random.randint(1, 7) * cell.width
            y = random.randint(1, 7) * cell.height
            enemy = Actor("enemy", topleft = (x, y))
            enemy.health = random.randint(15, 25)
            enemy.attack = random.randint(5, 10)
            enemy.bonus = random.randint(0, 2)
            enemies.append(enemy)
            if win == 2:
                mode = "end"
        
    elif char.health <= 0:
        mode = "end"
        win = -1


# Логика бонусов
def update(dt=0):
    if mode == "game":
        victory()
        for i in range(len(hearts)):
            if char.colliderect(hearts[i]):
                char.health += 5
                hearts.pop(i)
                break
            
        for i in range(len(swords)):
            if char.colliderect(swords[i]):
                char.attack += 5
                swords.pop(i)
                break
pgzrun.go()