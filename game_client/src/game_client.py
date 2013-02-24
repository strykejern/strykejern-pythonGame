import pygame;
import socket;
import time;
import sys;
import thread;
from pygame.locals import *;
from timer import Timer;
from shot import Shot;
from vector import Vector;
from math import pi;

def input(events):
    for event in events:
        if event.type == QUIT:
            pygame.quit();
            sys.exit(0);

class game_client:
    def __init__(self, address, motionblur):
        self.address = address;
        pygame.init();
        self.window = pygame.display.set_mode((800, 600));
        self.screen = pygame.display.get_surface();
        pygame.mouse.set_cursor(*pygame.cursors.diamond);
        self.fpsCounter = Timer(0);
        self.socket_init();
        self.ships = list();
        self.shots = list();
        self.motionblur = motionblur;
        if self.motionblur:
            self.ownBuffer = pygame.Surface((800, 600));
            self.ownBuffer.set_alpha(256-(255.0/motionblur));

        self.pntShip = (
            Vector(0,-10),
            Vector(0,10),
            Vector(30,0)
            );

        self.debugVar = None;
        thread.start_new_thread(self.debug, ());

    def run(self):
        while True:
            self.fpsCounter.update();
            input(pygame.event.get());
            if self.network(): break;
            Shot.updates(self.shots);
            self.draw();

        print "Lost connection to server";
        self.sock.close();

    def draw(self):
        self.screen.fill((0,0,0));
        if self.motionblur: self.screen.blit(self.ownBuffer, (0,0));
        for ship in self.ships:
            pos = Vector(ship[0][0], ship[0][1]);
            self.draw_ship(pos, ship[2] / 100.0);
        for shot in self.shots:
            pygame.draw.circle(self.screen, (0,255,0), shot.pos.get(1), 3);
        pygame.display.flip();
        if self.motionblur: self.ownBuffer.blit(self.screen, (0,0));

    def socket_init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        while self.sock.connect_ex((self.address, 1234)):
            print "Connection failed";
            time.sleep(5);
        print "Successful connection";
        self.sock.send("0");
        self.sock.recv(1024);
        
        

    def network(self):
        #keys = pygame.key.get_pressed();
        #self.sock.send(repr((0, keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_SPACE])));
        pos = pygame.mouse.get_pos();
        x = pos[0];
        y = pos[1];
        mshoot = pygame.mouse.get_pressed()[0];
        self.sock.send(repr((1, x, y, mshoot)))
        data = self.sock.recv(1024);
        if not data: return True;
        data = eval(data);
        # ([((50, 50), (0, 0), 0)], [])
        #print data;
        #time.sleep(2);
        self.ships = data[0];
        for shot in data[1]:
            pos = Vector(shot[0][0], shot[0][1]);
            speed = Vector(shot[1][0], shot[1][1]);
            self.shots.append(Shot(pos, speed));
        return False;

    def draw_ship(self, pos, angle):
        self.pntShip[0].rot_to(angle-(pi/2));
        self.pntShip[1].rot_to(angle+(pi/2));
        self.pntShip[2].rot_to(angle);

        pygame.draw.aalines(self.screen, (255, 0, 0), 1, (
            (pos.plus(self.pntShip[0]).get()),
            (pos.plus(self.pntShip[1]).get()),
            (pos.plus(self.pntShip[2]).get())
            ));

    def debug(self):
        while True:
            #print self.ships;
            time.sleep(2);