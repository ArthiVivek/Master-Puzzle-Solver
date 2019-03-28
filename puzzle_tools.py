"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# you may uncomment the next lines on a unix system such as CDF
import resource
resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


# TODO
# implement depth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like

def create_node_path(lst, index=0):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing a
    solution, with each child containing an extension of the puzzle in its
    parent. The index parameter keeps track of the current index of the list
    representation of the path (see docstrings of dfs_helper or bfs_helper for
    details about the path list).

    This is a helper function for both DFS and BFS.

    @param lst: list[Puzzle]
    @param index: int
    @return: PuzzleNode
    """
    if index == len(lst) - 1:
        return PuzzleNode(lst[index])
    else:
        return PuzzleNode(lst[index], [create_node_path(lst, index + 1)])


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent. Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None
    """

    # NOTE:
    #
    # For the three Sudoku puzzles in the starter code in
    # sudoku_puzzle.py, the first and third are solved rather quickly
    # (approx. 1 and 5 seconds respectively). The time needed for
    # the second Sudoku is around 5 to 20 seconds.
    #
    # For the grid peg puzzle in the starter code, it solves in about 5
    # seconds.

    def dfs_pathfinder(root):
        """
        Return a path from the input root puzzle to the solution, in the form
        of a list of puzzles where the first element is the root, the last
        element is the solution, and all elements in between are extensions
        in order that form the path. If no path is found, return None.

        @type root: Puzzle
        @rtype: list[Puzzle] | None
        """
        # initialise path, set of visited puzzle configurations, and stack
        path = [root]
        visited = set()
        visited.add(str(root))
        stack = [root]

        # while stack is not empty
        while stack:
            current_puzzle = stack[-1]
            # append the current puzzle to path if it is not the last path item
            if str(current_puzzle) != str(path[-1]):
                path.append(current_puzzle)
            # skip current_puzzle if it satisfies fail_fast
            if current_puzzle.fail_fast():
                del stack[-1]
                del path[-1]
                continue
            extensions = current_puzzle.extensions()
            # initialise counter to keep track of how many extensions of
            # current puzzle are already visited
            seen_count = 0
            # loop through the extensions of current puzzle
            for extension in extensions:
                if extension.is_solved():
                    path.append(extension)
                    return path
                elif str(extension) in visited:
                    seen_count += 1
                elif str(extension) not in visited:
                    visited.add(str(extension))
                    stack.append(extension)
            # if there are no extensions or all extensions are already visited
            if len(extensions) == 0 or seen_count == len(extensions):
                del stack[-1]
                del path[-1]
        return None

    if puzzle.is_solved():
        return PuzzleNode(puzzle)
    final_path = dfs_pathfinder(puzzle)
    # if a path is found
    if final_path:
        return create_node_path(final_path)
    else:
        return None

# TODO
# implement breadth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
# Hint: you may find a queue useful, that's why
# we imported deque


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None
    """

    def bfs_pathfinder(root):
        """
        Return a path from the input root puzzle to the solution, in the form
        of a list of puzzles where the first element is the root, the last
        element is the solution, and all elements in between are extensions
        in order that form the path. Return None if no path found.

        @param root: Puzzle
        @return: list[Puzzle] | None
        """
        # initialise set of visited puzzle configurations and queue of PATHS
        visited = set()
        visited.add(str(root))
        queue = deque()

        # Following code of this helper function is heavily modified from the
        # top answer in the web-page forum:
        # http://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a
        # -breadth-first-search

        # append to queue the current PATH LIST, not just the root itself
        queue.append([root])

        # while queue is not empty
        while queue:
            path = queue.popleft()
            # initialise the current puzzle as the last element of path
            current_puzzle = path[-1]
            if current_puzzle.is_solved():
                return path
            # loop through extensions of current puzzle
            for extension in current_puzzle.extensions():
                if str(extension) in visited:
                    continue
                elif extension.fail_fast():
                    visited.add(str(extension))
                else:
                    visited.add(str(extension))
                    # create a new_path by appending extension to current path
                    new_path = list(path) + [extension]
                    queue.append(new_path)
        return None

    final_path = bfs_pathfinder(puzzle)
    # if a path is found
    if final_path:
        return create_node_path(final_path)
    else:
        return None


def count_nodes(node):
    """
    Count number of nodes in tree.

    @param node: PuzzleNode
    @return: int
    """
    if not node:
        return 1
    else:
        return 1 + sum(count_nodes(child) for child in node.children)

# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.


class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other.

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
