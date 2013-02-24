from vector import Vector;

class Shot:
    def __init__(self, pos, speed, owner):
        self.pos = pos;
        self.speed = speed;
        self.speed.set_length(11);
        self.owner = owner;

    def update(self):
        self.pos.add(self.speed);
        if not self.pos.withinBounds(Vector(800, 600)).isNull():
            return False;
        return True;

    def to_data(self):
        return [(self.pos.get(1)), (self.speed.get(1))];

    @staticmethod
    def updates(shots):
        for i in range(len(shots)-1, -1, -1):
            if not shots[i].update():
                shots.pop(i);

    @staticmethod
    def net_pack(shots):
        data = list();
        for shot in shots:
            data.append(shot);
        return data;