import threading
import logging
import random
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


dato1 = 0
numLectores = 0

def Lector():
    global numLectores
    global dato1
    while True:
        numLectores += 1
        logging.info(f'Lector lee dato1 = {dato1}')
        time.sleep(1)
        numLectores -= 1
        time.sleep(random.randint(3,6))

def Escritor():
    global dato1
    while True:
        if numLectores == 0:
            dato1 = random.randint(0,100)
            logging.info(f'Escritor escribe dato1 = {dato1}')
        time.sleep(random.randint(1,4))


def main():
    nlector = 10
    nescritor = 2

    for k in range(nlector):
        threading.Thread(target=Lector, daemon=True).start()

    for k in range(nescritor):
        threading.Thread(target=Escritor, daemon=True).start()

    time.sleep(300)


if __name__ == "__main__":
    main()

