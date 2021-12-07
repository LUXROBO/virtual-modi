from time import sleep
from threading import Thread
from virtual_modi import VirtualBundle


vb = VirtualBundle()
vb.open()

def idle():
    sleep(0.01)

Thread(target=idle, daemon=True).start()

while True:
    sleep(0.01)

