import sys;
from game_client import game_client;

args = sys.argv[1:];

motionblur = 0;
address = '';

if len(args) < 2:
    motionblur = raw_input("Motionblur(0=off, max 255): ");
    if len(motionblur) == 0: motionblur = 0;
    else: motionblur = int(motionblur);

    if len(args) < 1:
        address = raw_input("Server address: ");
        if len(address) == 0: address = 'localhost';

    else: address = args[0];

else:
    address = args[0];
    motionblur = int(args[1]);


game = game_client(address, motionblur);
game.run();