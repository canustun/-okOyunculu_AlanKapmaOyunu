import zmq, random 
from tinyrpc.server import RPCServer
from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqServerTransport

ctx = zmq.Context()
dispatcher = RPCDispatcher()
transport = ZmqServerTransport.create(ctx, 'tcp://127.0.0.1:80')

rpc_server = RPCServer(
    transport,
    JSONRPCProtocol(),
    dispatcher)

konumlar = []
isimler = []
alan_x, alan_y = random.randint(0,50), random.randint(0,200)

@dispatcher.public
def index_bul(isim) -> int:
    return isimler.index(isim)

@dispatcher.public
def veri_temizleme(index):
    global konumlar, isimler
    konumlar.pop(index)
    isimler.pop(index)
    
@dispatcher.public
def liste_uzunlugu(x,y,isim,can):
    global isimler, konumlar
    if isim in isimler:
        return "Bu isim alınmış, Farklı bir isim dene!"
    else:
        isimler.append(isim)
        konumlar.append([x,y,can,isim])
        return len(konumlar)

@dispatcher.public
def sadece_iste_uzunlugu() -> int:
    return len(isimler)

@dispatcher.public
def konumlari_direk_cek():
    return konumlar

@dispatcher.public
def konum_al(x,y,index,can,isim) -> list:
    global konumlar
    konumlar[index] = [x,y,can,isim]
    return konumlar

@dispatcher.public
def alan_konum() -> list:
    return [alan_x, alan_y]

rpc_server.serve_forever()
