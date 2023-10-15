# Battleship game state tracker

from enum import Enum


class GameOver(Exception):
    pass


class DuplicateHit(Exception):
    pass


class OutOfBounds(Exception):
    pass


class Overlapping(Exception):
    pass


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Hit:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ship:
    def __init__(self, length, x, y, orientation, owner):
        if length <= 0:
            raise ValueError("Ship length must be positive and non-zero")
        self.length = length
        self.x = x
        self.y = y
        self.orientation = orientation
        self.hits = 0
        self.owner = owner


class Board:
    def __init__(self, height, width):
        self.hits = []
        self.height = height
        self.width = width
        self.ships = []

    def add_ship(self, ship):
        if ship.owner > 2 or ship.owner < 1:
            raise ValueError("Invalid owner")
        if ship.orientation == Orientation.HORIZONTAL:
            if ship.x + ship.length - 1 >= self.width:
                raise OutOfBounds()
        elif ship.orientation == Orientation.VERTICAL:
            if ship.y + ship.length - 1 >= self.height:
                raise OutOfBounds()

        for existing_ship in self.ships:
            existing_coords = [(existing_ship.x + (i if existing_ship.orientation == Orientation.HORIZONTAL else 0),
                                existing_ship.y + (i if existing_ship.orientation == Orientation.VERTICAL else 0))
                               for i in range(existing_ship.length)]

            new_coords = [(ship.x + (i if ship.orientation == Orientation.HORIZONTAL else 0),
                           ship.y + (i if ship.orientation == Orientation.VERTICAL else 0))
                          for i in range(ship.length)]

            if any(coord in existing_coords for coord in new_coords):
                raise Overlapping()

        self.ships.append(ship)

        return f'Ship added at ({ship.x},{ship.y})'

    def attack(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise OutOfBounds(f"Coordinates ({x},{y}) are out of board bounds")

        for hit in self.hits:
            if hit.x == x and hit.y == y:
                raise DuplicateHit()
        self.hits.append(Hit(x, y))

        for ship in self.ships:
            if ship.x <= x < ship.x + ship.length and ship.y == y and ship.orientation == Orientation.HORIZONTAL:
                ship.hits += 1
                if ship.hits == ship.length:
                    self.ships.remove(ship)
                    if self.is_game_over():
                        raise GameOver(f"Player {ship.owner} wins")
                return f'Hit at ({x},{y})'

            if ship.y <= y < ship.y + ship.length and ship.x == x and ship.orientation == Orientation.VERTICAL:
                ship.hits += 1
                if ship.hits == ship.length:
                    self.ships.remove(ship)
                    if self.is_game_over():
                        raise GameOver(f"Player {ship.owner} wins")
                return f'Hit at ({x},{y})'

        return f'Miss at ({x},{y})'

    def is_game_over(self):
        return len(set(ship.owner for ship in self.ships)) == 1


if __name__ == '__main__':
    board = Board(10, 10)

    # Example ship placement
    try:
        print(board.add_ship(Ship(5, 1, 0, Orientation.HORIZONTAL, 1)))
        print(board.add_ship(Ship(4, 0, 2, Orientation.VERTICAL, 1)))
        print(board.add_ship(Ship(3, 5, 5, Orientation.HORIZONTAL, 1)))
        print(board.add_ship(Ship(3, 0, 6, Orientation.VERTICAL, 2)))
        print(board.add_ship(Ship(4, 6, 1, Orientation.HORIZONTAL, 2)))
        print(board.add_ship(Ship(5, 8, 2, Orientation.VERTICAL, 2)))
    except (OutOfBounds, Overlapping, ValueError) as e:
        print(e.__class__.__name__)
        print(e.args[0])
        exit()

    # Example attacks
    try:
        print(board.attack(0, 0))
        print(board.attack(0, 1))
        print(board.attack(0, 2))
        print(board.attack(0, 3))
        print(board.attack(0, 4))
        print(board.attack(5, 5))
        print(board.attack(5, 6))
        print(board.attack(5, 7))
        print(board.attack(7, 2))
        print(board.attack(7, 3))
        print(board.attack(7, 4))
        print(board.attack(7, 5))
        print(board.attack(7, 6))
    except (GameOver, DuplicateHit, OutOfBounds) as e:
        print(e.__class__.__name__)
        print(e.args[0])
