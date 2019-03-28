from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid.

        @param MNPuzzle self: MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    # TODO
    # implement __eq__ and __str__
    # __repr__ is up to you

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @param self: MNPuzzle
        @param other: MNPuzzle | Any
        @return: bool

        >>> start_grid1 = (("*", "2", "3"), ("1", "4", "5"))
        >>> start_grid2 = (("1", "2", "3"), ("*", "4", "5"))
        >>> start_grid3 = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> puzzle1 = MNPuzzle(start_grid1, target_grid)
        >>> puzzle2 = MNPuzzle(start_grid2, target_grid)
        >>> puzzle3 = MNPuzzle(start_grid3, target_grid)
        >>> puzzle1 == puzzle2
        False
        >>> puzzle1 == puzzle3
        True
        """
        return (type(self) == type(other) and
                self.from_grid == other.from_grid and
                self.to_grid == other.to_grid)

    def __str__(self):
        """
        Return a user-friendly string representation of MNPuzzle self.

        @param self: MNPuzzle
        @return: str

        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> puzzle = MNPuzzle(start_grid, target_grid)
        >>> print(puzzle)
        From:
        * 2 3
        1 4 5
        To:
        1 2 3
        4 5 *
        """
        final_string = 'From:'
        for row in self.from_grid:
            final_string += '\n' + ' '.join(row)
        final_string += '\nTo:'
        for row in self.to_grid:
            final_string += '\n' + ' '.join(row)
        return final_string

    # TODO
    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"

    def extensions(self):
        """
        Return a list of extensions of MNPuzzle self.

        @param self: MNPuzzle
        @return: list[MNPuzzle]

        >>> start_grid = (("1", "*", "3"), ("2", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> puzzle = MNPuzzle(start_grid, target_grid)
        >>> for ext in puzzle.extensions():
        ...     print(ext)
        ...     print('-----')
        From:
        1 3 *
        2 4 5
        To:
        1 2 3
        4 5 *
        -----
        From:
        * 1 3
        2 4 5
        To:
        1 2 3
        4 5 *
        -----
        From:
        1 4 3
        2 * 5
        To:
        1 2 3
        4 5 *
        -----
        """
        final_list = []
        for row_num in range(self.n):
            for col_num in range(self.m):
                if self.from_grid[row_num][col_num] == '*':
                    # Case 1: symbol to the right of * exists
                    if col_num < self.m - 1:
                        changed_row = [x for x in self.from_grid[row_num]]
                        changed_row[col_num] = \
                            self.from_grid[row_num][col_num + 1]
                        changed_row[col_num + 1] = \
                            self.from_grid[row_num][col_num]
                        new_grid = []
                        for i in range(self.n):
                            if i != row_num:
                                new_grid.append(self.from_grid[i])
                            else:
                                new_grid.append(tuple(changed_row))
                        final_list.append(MNPuzzle(
                            tuple(new_grid), self.to_grid
                        ))
                    # Case 2: symbol to the left of * exists
                    if col_num > 0:
                        changed_row = [x for x in self.from_grid[row_num]]
                        changed_row[col_num] = \
                            self.from_grid[row_num][col_num - 1]
                        changed_row[col_num - 1] = \
                            self.from_grid[row_num][col_num]
                        new_grid = []
                        for i in range(self.n):
                            if i != row_num:
                                new_grid.append(self.from_grid[i])
                            else:
                                new_grid.append(tuple(changed_row))
                        final_list.append(MNPuzzle(
                            tuple(new_grid), self.to_grid
                        ))
                    # Case 3: symbol below * exists
                    if row_num < self.n - 1:
                        changed_row1 = [x for x in self.from_grid[row_num]]
                        changed_row2 = [x for x in self.from_grid[row_num + 1]]
                        changed_row1[col_num] = \
                            self.from_grid[row_num + 1][col_num]
                        changed_row2[col_num] = \
                            self.from_grid[row_num][col_num]
                        new_grid = []
                        for i in range(self.n):
                            if i == row_num:
                                new_grid.append(tuple(changed_row1))
                            elif i == row_num + 1:
                                new_grid.append(tuple(changed_row2))
                            else:
                                new_grid.append(self.from_grid[i])
                        final_list.append(MNPuzzle(
                            tuple(new_grid), self.to_grid
                        ))
                    # Case 4: symbol above * exists
                    if row_num > 0:
                        changed_row1 = [x for x in self.from_grid[row_num - 1]]
                        changed_row2 = [x for x in self.from_grid[row_num]]
                        changed_row1[col_num] = \
                            self.from_grid[row_num][col_num]
                        changed_row2[col_num] = \
                            self.from_grid[row_num - 1][col_num]
                        new_grid = []
                        for i in range(self.n):
                            if i == row_num - 1:
                                new_grid.append(tuple(changed_row1))
                            elif i == row_num:
                                new_grid.append(tuple(changed_row2))
                            else:
                                new_grid.append(self.from_grid[i])
                        final_list.append(MNPuzzle(
                            tuple(new_grid), self.to_grid
                        ))
        return final_list

    # TODO
    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid

    def is_solved(self):
        """
        Return whether MNPuzzle self is solved.

        @param self: MNPuzzle
        @return: bool

        >>> start_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> puzzle = MNPuzzle(start_grid, target_grid)
        >>> puzzle.is_solved()
        True
        """
        return self.from_grid == self.to_grid

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
