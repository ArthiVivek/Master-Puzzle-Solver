class Piece:
    """
    A piece used in Three Kingdoms puzzle.
    """

    def __init__(self, row, col):
        """
        Create a piece whose top-left coordinate is at (row, col).

        @param row: int
        @param col: int
        """
        assert 1 <= row and 1 <= col
        self.row = row
        self.col = col

    def __lt__(self, other):
        if self.row < other.row:
            return True
        elif self.row == other.row:
            return self.col < other.col
        else:
            return False

    def __le__(self, other):
        if self.row <= other.row:
            return True
        elif self.row == other.row:
            return self.col <= other.col
        else:
            return False

    def __gt__(self, other):
        if self.row > other.row:
            return True
        elif self.row == other.row:
            return self.col > other.col
        else:
            return False

    def __ge__(self, other):
        if self.row >= other.row:
            return True
        elif self.row == other.row:
            return self.col >= other.col
        else:
            return False

    def __str__(self):
        return str(type(self)) + ', ({}, {})'.format(self.row, self.col)


class BigSquare(Piece):
    """
    2x2 piece.
    """

    def __init__(self, row, col):
        assert row <= 4 and col <= 3
        super().__init__(row, col)


class SmallSquare(Piece):
    """
    1x1 piece.
    """

    def __init__(self, row, col):
        assert row <= 5 and col <= 4
        super().__init__(row, col)


class HorRec(Piece):
    """
    1x2 piece.
    """

    def __init__(self, row, col):
        assert row <= 5 and col <= 3
        super().__init__(row, col)


class VerRec(Piece):
    """
    2x1 piece.
    """

    def __init__(self, row, col):
        assert row <= 4 and col <= 4
        super().__init__(row, col)
