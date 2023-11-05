from tornado.ioloop import IOLoop

class mycontroller:
    def __init__(self):
        self.angle = 1
        self.throttle = 0.2
    
    def update(self):
        self.loop = IOLoop.instance()
        self.loop.start()

    def run_threaded(self):
        return self.angle,self.throttle

    def run(self):
        return self.run_threaded(self.angle,self.throttle)
