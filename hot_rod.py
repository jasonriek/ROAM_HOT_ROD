from hot_rod_driver import (Driver, sleep)
from hot_rod_sensors import (UltrasonicSensor)
from hot_rod_camera import (Camera)
from hot_rod_troubleshoot import (Troubleshoot)

class HotRod:
    def __init__(self):
        self.driver = Driver()
        self.ultrasonic_sensor = UltrasonicSensor()
        self.camera = Camera()
        self.troubleshoot = Troubleshoot()

    def sendUltrasonicSignal(self):
        return self.ultrasonic_sensor.read()

    def center(self):
        self.driver.center()

    def stop(self):
        self.driver.stop()
        sleep(1)

def test():
    hotrod = None
    counter = 0
    distance = 0
    try:
        hotrod = HotRod()
        speed = 10
        driving = True
        stuck_counter = 0
        

        hotrod.driver.driveForward(speed)
        while driving:

            signal = hotrod.sendUltrasonicSignal()
            if signal <= 40:
                hotrod.stop()
                sleep(2)
                #hotrod.camera.takeCollisionPhoto()
                hotrod.driver.turn90Degrees(Driver.RIGHT)
                hotrod.driver.driveForward(speed)
                print(counter)
                hotrod.troubleshoot.writeToCollisionTable(counter)
                if counter < 25:
                    hotrod.troubleshoot.collision_count += 1
                    if hotrod.troubleshoot.collision_count >= 5:
                        hotrod.driver.backup()
                        hotrod.troubleshoot.sendDistressToROAM()
                        hotrod.driver.driveForward(speed)
                else:
                    hotrod.troubleshoot.collision_count = 0
                counter = 0
                
            if hotrod.troubleshoot.isStuck():
                stuck_counter += 1
                if stuck_counter >= 3:
                    hotrod.driver.backup()
                    hotrod.troubleshoot.distance_cache.clear()
                    stuck_counter = 0

                
            counter += 1
            distance = round(signal)
            hotrod.troubleshoot.distance_cache.append(distance)
            print(f"distance: {round(signal)}")

    except KeyboardInterrupt:
        if hotrod:
            hotrod.center()
            hotrod.stop()
        
def sendSignalToRoam():
    hotrod = HotRod()
    hotrod.troubleshoot.sendDistressToROAM()     

def img_test():
    hotrod = HotRod()
    sleep(3)
    hotrod.camera.takeComparisionShot()
    hotrod.driver.backup()
    sleep(3)
    hotrod.camera.takeComparisionShot()
    hotrod.camera.compareShots()

img_test()
#test()
