from hot_rod_driver import Driver, sleep

class HotRod:
    def __init__(self):
        self.driver = Driver()

def test():
    hotrod = HotRod()
    hotrod.driver.driveForward(10)
    hotrod.driver.turnSharpLeft()
    sleep(3)
    hotrod.driver.stop()
    hotrod.driver.turnSharpRight()
    sleep(3)
    hotrod.driver.driveForward(10)
    hotrod.driver.center()
    hotrod.driver.stop()
    
    hotrod.driver.saveMotorSettings()

    '''
    hotrod.driver.driveForward(10)
    sleep(1)
    hotrod.driver.driveBackward(10)
    sleep(1)
    hotrod.driver.stop()
    '''
test()