import socket;
import thread;
import time;
from ship import Ship;
from timer import Timer;
from shot import Shot;
from vector import Vector;

class game_server:
    def __init__(self):
        self.connections = dict();
        self.ships = dict();
        self.shots = list();
        self.sendShots = dict();
        self.queueShots = dict();
        self.explosions = dict();
        self.fpsLimit = Timer(30);
        self.data = ();
        self.run = dict();
        self.sock_init();

        self.debugVar = None;
        thread.start_new_thread(self.debug, ());

    def start(self):
        thread.start_new_thread(self.listen, ());
        while True:
            if self.fpsLimit.update() and len(self.ships):

                for i in self.run:
                    self.run[i] = 1;
                Ship.updates(self.ships, self.shoot);
                Ship.collide(self.ships, self.shots, self.explosions);
                Shot.updates(self.shots);
                self.data = (Ship.to_data(self.ships));
            else:
                time.sleep(0.0005);

    def shoot(self, index):
        pos = self.ships[index].pos.copy();
        speed = Vector(1,1);
        speed.rot_to(self.ships[index].angle);
        self.shots.append(Shot(pos, speed, index));
        shotData = self.shots[-1].to_data();
        for i in self.queueShots:
            self.queueShots[i].append(shotData);

    def communicate(self, index):
        print "Connected to ", index;

        conn = self.connections[index];
        data = conn.recv(256);
        if not data: return;
        data = eval(data);

        time.sleep(1);

        conn.send(repr(((self.data), ())));

        while True:
            if self.run[index]:
                self.run[index] = 0;
                conn = self.connections[index];
                data = None;
                try: data = conn.recv(256);
                except: break;
                if not data: break;
                data = eval(data);
                if not data[0]: self.ships[index].set_keys(data[1], data[2], data[3], data[4], data[5]);
                else: self.ships[index].set_mouse((data[1], data[2]), data[3]);

                shots = Shot.net_pack(self.queueShots[index]);
                self.queueShots[index] = list();
                #shots = list();
                #while len(self.queueShots) > 1:
                #    shots.append(self.queueShots.pop());
                conn.send(repr((self.data, shots)));
        print "Client disconnected";
        self.connections[index].close();
        self.remove_player(index);

    def listen(self):
        while True:
            conn, addr              = self.sock.accept();
            self.connections[addr]  = conn;
            self.ships[addr]        = Ship();
            self.queueShots[addr]   = list();
            self.run[addr]          = 0;
            thread.start_new_thread(self.communicate, (addr,));

    def sock_init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.sock.bind(('', 1234));
        self.sock.listen(2);

    def remove_player(self, index):
        del self.connections[index];
        del self.ships[index];
        del self.run[index];
        del self.queueShots[index];

    def debug(self):
        while True:
            #print self.debugVar;
            time.sleep(2);
