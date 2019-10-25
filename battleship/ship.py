from enum import Enum


class ShipType(Enum):
    # values are tuple where first item is the representation on the board
    # and second value is the size of the ship
    CARRIER = ('C', 5)
    BATTLESHIP = ('B', 4)
    FRIGATE = ('F', 3)
    SUBMARINE = ('S', 3)
    DESTROYER = ('D', 2)


class Ship:
    def __init__(self, ship_type: ShipType):
        self.ship_type = ship_type
        self.size = self.ship_type.value[1]
        self.pieces = [ShipPiece(self.ship_type) for _ in range(self.size)]

    def is_destroyed(self) -> bool:
        return all([piece.hit for piece in self.pieces])

    def __repr__(self):
        return self.ship_type.name


class ShipPiece:
    def __init__(self, ship_type: ShipType):
        self.ship_type = ship_type
        self.hit = False

    def __repr__(self):
        return self.ship_type.value[0]
