from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type self: GridPegSolitairePuzzle
        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    # TODO
    # implement __eq__, __str__ methods
    # __repr__ is up to you

    def __eq__(self, other):
        """
        Return True if GridPegSolitairePuzzle self is equivalent to other.

        @param self: GridPegSolitairePuzzle
        @param other: GridPegSolitairePuzzle | Any
        @return: bool

        >>> grid1 = [["*", "*", "*", "*", "*"],
        ...          ["*", "*", "*", "*", "*"],
        ...          ["*", "*", ".", "*", "*"],
        ...          ["*", "*", "*", "*", "*"],
        ...          ["*", "*", "*", "*", "*"]]
        >>> grid2 = [["*", "*", "*", "*", "*"],
        ...          ["*", "*", "*", "*", "*"],
        ...          ["*", "*", ".", "*", "*"],
        ...          ["*", "*", "*", "*", "*"]]
        >>> grid3 = [["*", "*", "*", "*", "*"],
        ...          ["*", "*", "*", "*", "*"],
        ...          ["*", "*", ".", "*", "*"],
        ...          ["*", "*", "*", "*", "*"],
        ...          ["*", "*", "*", "*", "*"]]
        >>> puzzle1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> puzzle2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> puzzle3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> puzzle1 == puzzle2
        False
        >>> puzzle1 == puzzle3
        True
        """
        return (type(self) == type(other) and
                self._marker == other._marker and
                self._marker_set == other._marker_set)

    def __str__(self):
        """
        Return a user-friendly string representation of GridPegSolitaire self.

        @param self: GridPegSolitairePuzzle
        @return: str

        >>> grid = [["*", "*", "*", "*", "*"],
        ...         ["*", "*", "*", "*", "*"],
        ...         ["*", "*", ".", "*", "*"],
        ...         ["*", "*", "*", "*", "*"],
        ...         ["*", "*", "*", "*", "*"]]
        >>> print(GridPegSolitairePuzzle(grid, {"*", ".", "#"}))
        * * * * *
        * * * * *
        * * . * *
        * * * * *
        * * * * *
        """
        final_string = ''
        for row_num in range(len(self._marker)):
            for entry_num in range(len(self._marker[row_num])):
                final_string += self._marker[row_num][entry_num]
                if entry_num != len(self._marker[row_num]) - 1:
                    final_string += ' '
            if row_num != len(self._marker) - 1:
                final_string += '\n'
        return final_string

    # TODO
    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration

    def extensions(self):
        """
        Return a list of extensions of GridPegSolitaire self.

        @param self: GridPegSolitairePuzzle
        @return: list[GridPegSolitairePuzzle]

        >>> grid = [["*", "*", "*", "*", "*"],
        ...         ["*", "*", "*", "*", "*"],
        ...         ["*", "*", ".", "*", "*"]]
        >>> puzzle = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> for ext in puzzle.extensions():
        ...     print(ext)
        ...     print('---------')
        * * * * *
        * * * * *
        . . * * *
        ---------
        * * * * *
        * * * * *
        * * * . .
        ---------
        * * . * *
        * * . * *
        * * * * *
        ---------
        """
        final_list = []

        # Case 1: Horizontal (peg peg empty / empty peg peg)
        if len(self._marker[0]) >= 3:
            for row_num in range(len(self._marker)):
                target_row = self._marker[row_num]
                for col_num in range(len(target_row) - 2):
                    # if order is (peg peg empty)
                    if (target_row[col_num] == '*' and
                            target_row[col_num + 1] == '*' and
                            target_row[col_num + 2] == '.'):
                        changed_row = [item for item in target_row]
                        # independent copy of target row for alterations
                        changed_row[col_num] = '.'
                        changed_row[col_num + 1] = '.'
                        changed_row[col_num + 2] = '*'
                        new_grid = (self._marker[:row_num] +
                                    [changed_row] +
                                    self._marker[row_num + 1:])
                        final_list.append(GridPegSolitairePuzzle(
                            new_grid, self._marker_set
                        ))
                    # if order is (empty peg peg):
                    elif (target_row[col_num] == '.' and
                            target_row[col_num + 1] == '*' and
                            target_row[col_num + 2] == '*'):
                        changed_row = [item for item in target_row]
                        changed_row[col_num] = '*'
                        changed_row[col_num + 1] = '.'
                        changed_row[col_num + 2] = '.'
                        new_grid = (self._marker[:row_num] +
                                    [changed_row] +
                                    self._marker[row_num + 1:])
                        final_list.append(GridPegSolitairePuzzle(
                            new_grid, self._marker_set
                        ))

        # Case 2: Vertical (peg peg empty / empty peg peg)
        if len(self._marker) >= 3:
            for col_num in range(len(self._marker[0])):
                for row_num in range(len(self._marker) - 2):
                    # if order is (peg peg empty):
                    if (self._marker[row_num][col_num] == '*' and
                            self._marker[row_num + 1][col_num] == '*' and
                            self._marker[row_num + 2][col_num] == '.'):
                        changed_row_1 = [item for item in
                                         self._marker[row_num]]
                        changed_row_2 = [item for item in
                                         self._marker[row_num + 1]]
                        changed_row_3 = [item for item in
                                         self._marker[row_num + 2]]
                        changed_row_1[col_num] = '.'
                        changed_row_2[col_num] = '.'
                        changed_row_3[col_num] = '*'
                        new_grid = (self._marker[:row_num] +
                                    [changed_row_1] +
                                    [changed_row_2] +
                                    [changed_row_3] +
                                    self._marker[row_num + 3:])
                        final_list.append(GridPegSolitairePuzzle(
                            new_grid, self._marker_set
                        ))
                    # if order is (empty peg peg):
                    elif (self._marker[row_num][col_num] == '.' and
                            self._marker[row_num + 1][col_num] == '*' and
                            self._marker[row_num + 2][col_num] == '*'):
                        changed_row_1 = [item for item in
                                         self._marker[row_num]]
                        changed_row_2 = [item for item in
                                         self._marker[row_num + 1]]
                        changed_row_3 = [item for item in
                                         self._marker[row_num + 2]]
                        changed_row_1[col_num] = '*'
                        changed_row_2[col_num] = '.'
                        changed_row_3[col_num] = '.'
                        new_grid = (self._marker[:row_num] +
                                    [changed_row_1] +
                                    [changed_row_2] +
                                    [changed_row_3] +
                                    self._marker[row_num + 3:])
                        final_list.append(GridPegSolitairePuzzle(
                            new_grid, self._marker_set
                        ))
        return final_list

    # TODO
    # override is_solved
    # A configuration is solved when there is exactly one "*" left

    def is_solved(self):
        """
        Return whether GridPegSolitairePuzzle self is solved.

        @param self: GridPegSolitairePuzzle
        @return: bool

        >>> grid = [[".", ".", ".", "*", "."],
        ...         [".", ".", ".", ".", "."],
        ...         [".", ".", ".", ".", "."]]
        >>> puzzle = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> puzzle.is_solved()
        True
        """
        peg_count = 0
        for row in self._marker:
            for item in row:
                if item == '*':
                    peg_count += 1
        return peg_count == 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
