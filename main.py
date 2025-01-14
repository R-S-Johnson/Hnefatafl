from gameController import GameController
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='Hnefatafl Game',
        description='Simulation of Hnefatafl game with ML back-end',
    )
    parser.add_argument(
        '--debug-mode', action='store_true',
        help="unadvised without knowledge on the structure of the needed debug-logs folder and files",
    )
    args = parser.parse_args()
    
    controller = GameController(args.debug_mode)
    controller.mainLoop()
    
if __name__ == "__main__":
    main()