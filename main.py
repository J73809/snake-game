from pygame import *
from random import randint
from time impport sleep

# --- Player ---
direction = 'right'
size = 50
color = (18, 222, 18)
player = Rect(50, 50, size, size)
score = 0
grow = True
die = False
tail = []
color3 = (18, 200, 30)
timer = 1

# --- Window ---
width, height = 16 * size, 16 * size
scr = display.set_mode((width, height))
display.set_caption('Snake')
icon = image.load('assets/icon/icon.png')
display.set_icon(icon)

# --- Apple ---
apple = Rect(300, 300, size, size)
color2 = (222, 18, 18)

# --- Sound ---
mixer.init()

mixer.music.load('assets/sound/background.wav')
mixer.music.set_volume(0.8)

bite = mixer.Sound('assets/sound/bite.wav')
lose = mixer.Sound('assets/sound/lose.wav')

# --- Function ---
def core():
    global direction, score, grow, run, die, timer, game_state
    
    tail.insert(0, player.copy())
    
    if not grow:
        tail.pop()
    else:
        grow = False
        
    if die:
        timer -= 1
        if timer == 0:
            if tail:
                tail.pop()
                timer = 1
        else:
            die = False
            game_state = 'dead'
    
    keys = key.get_pressed()
    next_direction = direction
    if keys[K_w] or keys[K_UP] and direction != 'down':
        next_direction = 'up'
    elif keys[K_a] or keys[K_LEFT] and direction != 'right':
        next_direction = 'left'
    elif keys[K_s] or keys[K_DOWN] and direction != 'up':
        next_direction = 'down'
    elif keys[K_d] or keys[K_RIGHT] and direction != 'left':
        next_direction = 'right'
    direction = next_direction
        
    if direction == 'up':
        player.y -= size
    elif direction == 'left':
        player.x -= size
    elif direction == 'down':
        player.y += size
    elif direction == 'right':
        player.x += size
        
    if player.left < 0:
        player.right = width
    elif player.right > width:
        player.left = 0
    elif player.top < 0:
        player.bottom = height
    elif player.bottom > height:
        player.top = 0
    
    if player.colliderect(apple):
        bite.play()
        score += 1
        grow = True
        while 1:
            apple.x = randint(0, 15) * size
            apple.y = randint(0, 15) * size
            if all(apple.x != segment.x or apple.y != segment.y for segment in tail):
                break
        
    for segment in tail[1: ]:
        if player.colliderect(segment):
            direction = '0'
            mixer.music.stop()
            if not die:
                lose.play()
            die = True

# --- Main parameters ---
run = True

clock = time.Clock()
FPS = 9

# --- Font ---
font.init()
font0 = font.Font(None, 40)
start = font.Font(None, 45)

# --- Main game ---
game_state = 'start'

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if game_state == 'start' and e.key == K_SPACE:
                game_state = 'play'
                mixer.music.play(-1)
            elif game_state == 'dead' and e.key == K_SPACE:
                player.x = 50
                player.y = 50
                direction = 'right'
                apple.x = 300
                apple.y = 300
                score = 0
                grow = True
                die = False
                tail.clear()
                timer = 1
                game_state = 'start'
            elif game_state == 'dead' and e.key == K_q:
                time.delay(300)
                run = False
    
    mouse.set_visible(False) 
    scr.fill((0, 0, 0))
    
    if game_state == 'start':
        text2 = start.render('SPACE - start', True, (255, 255, 255))
        scr.blit(text2, (width // 2 - text2.get_width() // 2, height - size * 4))
    elif game_state == 'play':        
        core()
    elif game_state == 'dead':
        text3 = start.render('SPACE - restart / Q - quit', True, (255, 255, 255))
        scr.blit(text3, (width // 2 - text3.get_width() // 2, height - size * 4))
    
    for segment in tail:
        draw.rect(scr, color3, segment)
    
    text = font0.render(f'Score: {score}', True, (255, 255, 255))
    scr.blit(text, (15, 15))
    
    draw.rect(scr, color, player)
    draw.rect(scr, color2, apple)
    
    display.update()
    clock.tick(FPS)

quit()