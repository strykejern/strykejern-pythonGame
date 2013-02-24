from math import sqrt, cos, sin, atan2, radians, degrees;

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x;
        self.y = y;

    def set(self, vec):
        #if vec.type == "vector":
        self.x = vec.x;
        self.y = vec.y;
        #elif vec.type == "array":
        #    self.x = vec[0];
        #    self.y = vec[1];

    def add(self, vec):
        self.x += vec.x;
        self.y += vec.y;

    def sub(self, vec):
        self.x -= vec.x;
        self.y -= vec.y;

    def mul(self, num):
        self.x *= num;
        self.y *= num;

    def div(self, num):
        self.x /= num;
        self.y /= num;

    def plus(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y);

    def minus(self, vec):
        return Vector(self.x - vec.x, self.y - vec.y);

    def multiplied(self, num):
        return Vector(self.x * num, self.y * num);

    def divided(self, num):
        return Vector(self.x / num, self.y / num);

    def negate(self):
        self.x = -self.x;
        self.y = -self.y;

    def hflip(self):
        self.x = -self.x;

    def vflip(self):
        self.y = -self.y;

    def get(self, round=0):
        if round:
            return [int(self.x), int(self.y)];
        else:
            return (self.x, self.y);

    def copy(self):
        return Vector(self.x, self.y);

    def equal(self, vect):
        if self.x == vect.x and self.y == vect.y:
            return True;
        return False;

    def isNull(self):
        if self.x == 0 and self.y == 0:
            return True;
        return False;

    def withinBounds(self, bounds):
        x = 0;
        y = 0;
        if self.x < 0:
            x = -self.x;
        elif self.x > bounds.x:
            x = bounds.x - self.x;
        if self.y < 0:
            y = -self.y; 
        elif self.y > bounds.y:
            y = bounds.y - self.y;
        return Vector(x, y);

    def moveWithinBounds(self, bounds):
        move = self.withinBounds(bounds);
        self.add(move);
        if   move.x: return 1;
        elif move.y: return 2;
        return 0;

    def hyp(self):
        return sqrt((self.x**2)+(self.y**2));

    def set_length(self, length):
        hyp = self.hyp();
        fx = self.x / hyp;
        fy = self.y / hyp;
        self.x = fx * length;
        self.y = fy * length;

    def rot_deg(self, deg):
        self.x = (cos(radians(deg)) * self.x) - (sin(radians(deg)) * self.y);
        self.y = (sin(radians(deg)) * self.x) + (cos(radians(deg)) * self.y);

    def rot(self, rad):
        self.x = (cos(rad) * self.x) - (sin(rad) * self.y);
        self.y = (sin(rad) * self.x) + (cos(rad) * self.y);

    def rot_to_deg(self, deg):
        length = self.hyp();
        self.x = cos(radians(deg)) * length;
        self.y = sin(radians(deg)) * length;

    def rot_to(self, rad):
        length = self.hyp();
        self.x = cos(rad) * length;
        self.y = sin(rad) * length;

    def angle_deg(self):
        return degrees(atan2(self.y, self.x));

    def angle(self):
        return atan2(self.y, self.x);

    def dist_to(self, vec):
        tmpVec = Vector(self.x - vec.x, self.y - vec.y);
        return tmpVec.hyp();