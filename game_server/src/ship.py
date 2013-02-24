from vector import Vector;
from timer import Timer;

class Ship:
    def __init__(self, x=50, y=50):
        self.pos = Vector(x, y);
        self.speed = Vector();
        self.accel = Vector();
        self.angle = 0;
        self.tmpAngle = 0;
        self.canShoot = 1;
        self.shootLimiter = Timer(2);
        self.keyb = 1;

        self.keys = {
            "up":0,
            "down":0,
            "left":0,
            "right":0,
            "shoot":0
            };
        self.mouse = Vector(0,0);
        self.mShoot = 0;
        
        self.accel.x = 1;
        self.points = (
            Vector(0,-10),
            Vector(0,10),
            Vector(30,0)
            );

    def update(self, shoot_function, index):
        if self.canShoot:
            self.shootLimiter.reset();
        else:
            self.canShoot = self.shootLimiter.update();
        if self.keyb:
            if self.keys["up"]:       self.accel.y = -0.5;
            elif self.keys["down"]:   self.accel.y = 0.5;
            else:
                self.accel.y = 0;
                self.speed.y *= 0.98;
            if self.keys["left"]:     self.accel.x = -0.5;
            elif self.keys["right"]:  self.accel.x = 0.5;
            else:
                self.accel.x = 0;
                self.speed.x *= 0.98;
            if self.keys["shoot"] and self.canShoot:
                self.canShoot = 0;
                self.shootLimiter.reset();
                shoot_function(index);
        else:
            if self.accel.hyp() < 1: self.accel = Vector(0,1);
            self.accel.rot_to(self.mouse.minus(self.pos).angle());
            if self.mshoot and self.canShoot:
                self.canShoot = 0;
                self.shootLimiter.reset();
                shoot_function(index);

        if not self.accel.isNull(): self.angle = self.accel.angle();
        self.speed.add(self.accel);
        if not self.speed.isNull():
            hyp = self.speed.hyp();
            if hyp > 10:
                self.speed.set_length(10);
            
        self.pos.add(self.speed);
        bounce = self.pos.moveWithinBounds(Vector(800, 600));
        if bounce:
            if bounce   == 1: self.speed.x = -self.speed.x;
            elif bounce == 2: self.speed.y = -self.speed.y;

    def hit(self):
        pass;

    def set_keys(self, up, down, left, right, shoot):
        self.keyb = 1;
        self.keys["up"] = up;
        self.keys["down"] = down;
        self.keys["left"] = left;
        self.keys["right"] = right;
        self.keys["shoot"] = shoot;

    def set_mouse(self, mpos, mshoot):
        self.keyb = 0;
        self.mouse.x = mpos[0];
        self.mouse.y = mpos[1];
        self.mshoot = mshoot;
    
    def net_data(self):
        # [0] = ( posX, posY )
        # [1] = ( speedX, speedY )
        # [2] = angle
        # ( ( posX, posY ), ( speedX, speedY ), angle )
        return (self.pos.get(1), self.speed.get(1), int(self.angle * 100));

    @staticmethod
    def collide(ships, shots, explosions=0):
        for i in ships:
            for shot in shots:
                if ships[i].pos.dist_to(shot.pos) < 10:
                    ships[i].hit();

    @staticmethod
    def updates(ships, shoot_function):
        for i in ships:
            ships[i].update(shoot_function, i);

    @staticmethod
    def to_data(ships):
        data = list();
        for i in ships:
            data.append(ships[i].net_data());
        return data;
