import zmq, pygame, sys, timeit
from random import randint,choice
from tinyrpc import RPCClient
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from time import sleep
from threading import Thread

pygame.init()
ctx = zmq.Context()

rpc_client = RPCClient(
    JSONRPCProtocol(),
    ZmqClientTransport.create(ctx, 'tcp://127.0.0.1:80'))
server = rpc_client.get_proxy()

harfler = "abcçdefgğhıijklmnoöprsştüuvyzwqx"
while 1:
    uzunluk = server.sadece_iste_uzunlugu()
    if uzunluk < 3:
        isim = choice(harfler)#input("İsminiz :")
        x, y = randint(0,600),randint(0,600)

        index = server.liste_uzunlugu(x,y,isim,100)
        if index == "Bu isim alınmış, Farklı bir isim dene!":
            print(index)
            continue
        alan_x,alan_y = server.alan_konum()
        index = server.index_bul(isim)
        konum = server.konum_al(x,y,index,100,isim)
        break
    else:sys.exit(1)
    
alan_buyuklugu = 400
def alan_azalma():
    global alan_buyuklugu,bsl_zmn, canımız
    while alan_buyuklugu>0:
        sleep(1)
        gecen_sure = int(float(str(bsl_zmn - timeit.default_timer())[1:]))
        alan_buyuklugu -= gecen_sure*7
        try:    
            if gecen_sure>1.2 and not biz.colliderect(alan):
                canımız-=25*gecen_sure
        except:pass

        bsl_zmn = timeit.default_timer()

fps = pygame.time.Clock()
izleyici_modu = None
uzunluk_kont = True
olduk = False
canımız = 100
font = pygame.font.SysFont("Consolas",15)
ekran = pygame.display.set_mode((800,800))
calis, threadi_calistir = 1, 1

while calis:
    ekran.fill("black")
    
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            calis = 0
    liste_uzunluk = server.sadece_iste_uzunlugu()

    if liste_uzunluk < 3 and uzunluk_kont:
        ekran.blit(font.render("Diğer Oyuncular Bekleniyor...",True,("White")),(350,400))
        
    else:
        alan = pygame.draw.rect(ekran, ("green"),[alan_x,alan_y,alan_buyuklugu*2, alan_buyuklugu*2], 3)
        uzunluk_kont = False
        if threadi_calistir:
            bsl_zmn = timeit.default_timer()
            Thread(target = alan_azalma).start()
            threadi_calistir = 0
        elif not izleyici_modu:
            index = server.index_bul(isim)
            
            tıklamalar = pygame.key.get_pressed()
            if tıklamalar[pygame.K_a] and x>0:x-=1
            elif tıklamalar[pygame.K_d] and x<775:x+=1
                
            if tıklamalar[pygame.K_w] and y>0:y-=1
            elif tıklamalar[pygame.K_s] and y<775:y+=1
            konum = server.konum_al(x,y,index,canımız,isim)
            biz = pygame.draw.rect(ekran,("White"),pygame.Rect(x,y,25,25))
                    
            if not biz.colliderect(alan):canımız-=0.5
            else:
                if canımız<100:canımız+=0.002

            #oyuncuları göster
            for i in konum:
                pygame.draw.rect(ekran,("White"),pygame.Rect(i[0],i[1],25,25))
                ekran.blit(font.render(str(int(i[2])),True,("Yellow")),(i[0]+1,i[1]-15))
        
        if canımız <= 0 and not izleyici_modu:
            server.veri_temizleme(index)
            izleyici_modu = True
        else:
            direk_konumlar = server.konumlari_direk_cek()
            for i in direk_konumlar:
                pygame.draw.rect(ekran,("White"),pygame.Rect(i[0],i[1],25,25))
                ekran.blit(font.render(str(int(i[2])),True,("Yellow")),(i[0]+1,i[1]-15))
                ekran.blit(font.render(i[3][:5],True,("Cyan")),(i[0]-7,i[1]+25))

    pygame.display.update()
    fps.tick(150)
