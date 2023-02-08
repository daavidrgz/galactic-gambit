import sys
# workarround in order to modify PYTHONPATH env var.
# Alternative to this is to run `PYTHONPATH=src python3 run_game.py` instead
sys.path.append('src')

import game

if __name__ == '__main__':
    game.run()