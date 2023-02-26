'''
from picarx import Picarx
from time import sleep

def main():
    moving = True
    try:
        px = Picarx()
        while moving:
            distance = px.ultrasonic.read()
            print(f'distance: {distance}')
            px.forward(10)
            if distance > 0 and distance <= 20:
                px.forward(0)
                moving = False
        
        sleep(3)
        moving = True
        while moving:
            distance = px.ultrasonic.read()
            print(f'distance: {distance}')
            px.backward(10)
            if distance >= 60:
                px.backward(0)
                moving = False
    finally:
        px.forward(0)
        px.stop()

if __name__ == "__main__":
    main()
'''