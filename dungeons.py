#pgzero
import random
# Pencerenin Çizimi
hucre = Actor("sınır")
hucre1 = Actor("zemin")
hucre2 = Actor("çatlak")
hucre3 = Actor("kemikler")
ekran_g = 9 # Ekranın enindeki hücre sayısı
ekran_y = 10 # Ekranın boyundaki hücre sayısı
WIDTH = hucre.width * ekran_g
HEIGHT = hucre.height * ekran_y
mod = "oyun"

TITLE = "Zindanlar" # Oyunun Adı
FPS = 30 # Saniyedeki Kare Sayısı
haritam = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 1, 1, 2, 1, 3, 1, 1, 0], 
          [0, 1, 1, 1, 2, 1, 1, 1, 0], 
          [0, 1, 3, 2, 1, 1, 3, 1, 0], 
          [0, 1, 1, 1, 1, 3, 1, 1, 0], 
          [0, 1, 1, 3, 1, 1, 2, 1, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [-1, -1, -1, -1, -1, -1, -1, -1, -1]] # Hücüm Gücü ve Sağlık bilgisi

# Başrol Karakteri
karakter = Actor('karakter')
karakter.health = 100
karakter.attack = 5
karakter.top = hucre.height
karakter.left = hucre.width

dusmanlar = []
for i in range(5):
    x = random.randint(1,7) * hucre.width
    y = random.randint(1,7) * hucre.height
    dusman = Actor("düşman", topleft = (x,y))
    dusman.health = random.randint(10,20)
    dusman.attack = random.randint(5,10)
    dusman.bonus = random.randint(0,2)
    dusmanlar.append(dusman)
    
kalpler = []
kiliclar = []


def harita_cizim():
    for i in range(len(haritam)):
        for j in range(len(haritam[0])):
            if haritam[i][j] == 0:
                hucre.left = hucre.width*j
                hucre.top = hucre.height*i
                hucre.draw()
            elif haritam[i][j] == 1:
                hucre1.left = hucre.width*j
                hucre1.top = hucre.height*i
                hucre1.draw()
            elif haritam[i][j] == 2:
                hucre2.left = hucre.width*j
                hucre2.top = hucre.height*i
                hucre2.draw()  
            elif haritam[i][j] == 3:
                hucre3.left = hucre.width*j
                hucre3.top = hucre.height*i
                hucre3.draw() 

def draw():
    if mod == "oyun":
        screen.fill("#2f3542")
        harita_cizim()
        karakter.draw()
        screen.draw.text("Sağlık:", center=(35, 475), color = 'white', fontsize = 20)
        screen.draw.text(karakter.health, center=(85, 475), color = 'white', fontsize = 20)
        screen.draw.text("Hücum:", center=(375, 475), color = 'white', fontsize = 20)
        screen.draw.text(karakter.attack, center=(425, 475), color = 'white', fontsize = 20)
        for i in range(len(dusmanlar)):
            dusmanlar[i].draw()
        for i in range(len(kalpler)):
            kalpler[i].draw()
        for i in range(len(kiliclar)):
            kiliclar[i].draw()
    if mod == "son":
        screen.fill("#2f3542")
        if kazanmak == 1:
            screen.draw.text("KAZANDINIZ!", center=(WIDTH/2, HEIGHT/2), color ="white", fontsize =46)
        else:
            screen.draw.text("KAYBETTINIZ!", center=(WIDTH/2, HEIGHT/2), color ="white", fontsize =46)

def on_key_down(key):
    eski_x = karakter.x
    eski_y = karakter.y
    if keyboard.right and karakter.x + hucre.width < WIDTH - hucre.width:
        karakter.x += hucre.width
        karakter.image = 'karakter'
    elif keyboard.left and karakter.x - hucre.width > hucre.width:
        karakter.x -= hucre.width
        karakter.image = 'sol'
    elif keyboard.down and karakter.y + hucre.height < HEIGHT - hucre.height*2:
        karakter.y += hucre.height
    elif keyboard.up and karakter.y - hucre.height > hucre.height:
        karakter.y -= hucre.height
        
    dusman_sira = karakter.collidelist(dusmanlar)
    if dusman_sira != -1:
        karakter.x = eski_x
        karakter.y = eski_y
        dusman = dusmanlar[dusman_sira]
        dusman.health -= karakter.attack
        karakter.health -= dusman.attack
        if dusman.health <= 0:
            if dusman.bonus == 1:
                kalp = Actor("kalp")
                kalp.pos = dusman.pos
                kalpler.append(kalp)
            elif dusman.bonus == 2:
                kilic = Actor("kılıç")
                kilic.pos = dusman.pos
                kiliclar.append(kilic)
            dusmanlar.pop(dusman_sira)
            
            
def zafer():
    global mod, kazanmak
    if karakter.health > 0 and dusmanlar == []:
        mod = "son"
        kazanmak = 1
    elif karakter.health <= 0:
        mod = "son"
        kazanmak = 0
    
def update(dt):
    zafer()
    for i in range(len(kalpler)):
        if karakter.colliderect(kalpler[i]):
            karakter.health += 5
            kalpler.pop(i)
            break
    for i in range(len(kiliclar)):
        if karakter.colliderect(kiliclar[i]):
            karakter.attack += 5
            kiliclar.pop(i)
            break
