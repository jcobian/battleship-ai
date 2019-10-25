class Ship:
    def __init__(self, ship_type, size):
        self.ship_type = ship_type
        self.size = size
        self.pieces = [ShipPiece(self.ship_type) for _ in range(size)]

    def is_destroyed(self):
        return all([piece.hit for piece in self.pieces])


class ShipPiece:
    def __init__(self, ship_type):
        self.ship_type = ship_type
        self.hit = False

    def __repr__(self):
        return self.ship_type[0]
