import time;

class Timer:
    tmpTime = 0
    timeNow = 0
    fps     = 0.0
    counter = 0
    delay   = 0
    diffTime= 0
    timer   = 0

    def __init__(self, fps=0):
        self.isCounter = 0;
        self.tmpTime = time.clock();
        if fps != 0:
            self.delay = 1.0/fps;
            print 1.0/self.delay, " fps";
        else: self.isCounter = 1;

    def reset(self):
        self.timer = 0;
        self.counter = 0;

    def update(self):
        self.timeNow = time.clock();
        self.timer += (self.timeNow - self.diffTime);
        self.diffTime = self.timeNow;
        if self.timer > self.delay:
            self.timer = 0;
            self.counter += 1;
            if self.counter == 10:
                if self.isCounter: self.fps = 10.0 / (self.timeNow - self.tmpTime);
                self.tmpTime = self.timeNow;
                self.counter = 0;
            return True;
        return False;