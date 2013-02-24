from vector import Vector;

class Shot:
    def __init__(self, pos, speed):
        self.pos = pos;
        self.speed = speed;

    def update(self):
        self.pos.add(self.speed);
        if not self.pos.withinBounds(Vector(800, 600)).isNull():
            return False;
        return True;

    @staticmethod
    def updates(shots):
        for i in range(len(shots)-1, -1, -1):
            if not shots[i].update():
                shots.pop(i);