from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type self: WordLadderPuzzle
        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    # TODO
    # implement __eq__ and __str__
    # __repr__ is up to you

    def __eq__(self, other):
        """
        Return True if WordLadderPuzzle self is equivalent to other.

        @param self: WordLadderPuzzle
        @param other: WordLadderPuzzle | Any
        @return: bool

        >>> puzzle1 = WordLadderPuzzle("meow", "woof", {"hello", "goodbye"})
        >>> puzzle2 = WordLadderPuzzle("meow", "bark", {"hello", "goodbye"})
        >>> puzzle3 = WordLadderPuzzle("meow", "woof", {"hello", "goodbye"})
        >>> puzzle1 == puzzle2
        False
        >>> puzzle1 == puzzle3
        True
        """
        return (type(self) == type(other) and
                self._from_word == other._from_word and
                self._to_word == other._to_word and
                self._word_set == other._word_set)

    def __str__(self):
        """
        Return a user-friendly string representation of WordLadderPuzzle self.

        @param self: WordLadderPuzzle
        @return: str

        >>> puzzle = WordLadderPuzzle("computer", "science", {"fun"})
        >>> print(puzzle)
        From 'computer' to 'science'
        """
        return "From '{}' to '{}'".format(self._from_word, self._to_word)

    # TODO
    # override extensions
    # legal extensions are WordPadderPuzzles that have a from_word that can
    # be reached from this one by changing a single letter to one of those
    # in self._chars

    def extensions(self):
        """
        Return a list of extensions of WordLadderPuzzle self.

        @param self: WordLadderPuzzle
        @return: list[WordLadderPuzzle]

        >>> with open("words", "r", encoding='UTF-8') as words:
        ...     word_set = set(words.read().split())
        >>> puzzle = WordLadderPuzzle("same", "cost", word_set)
        >>> for ext in puzzle.extensions():
        ...     print(ext)
        From 'came' to 'cost'
        From 'dame' to 'cost'
        From 'fame' to 'cost'
        From 'game' to 'cost'
        From 'lame' to 'cost'
        From 'name' to 'cost'
        From 'tame' to 'cost'
        From 'some' to 'cost'
        From 'safe' to 'cost'
        From 'sage' to 'cost'
        From 'sake' to 'cost'
        From 'sale' to 'cost'
        From 'sane' to 'cost'
        From 'sate' to 'cost'
        From 'save' to 'cost'
        """
        final_list = []
        for index in range(len(self._from_word)):
            for char in self._chars:
                possible_ext = [letter for letter in self._from_word]
                possible_ext[index] = char
                possible_word = ''.join(possible_ext)
                if (possible_word in self._word_set and
                        possible_word != self._from_word):
                    final_list.append(
                        WordLadderPuzzle(possible_word,
                                         self._to_word,
                                         self._word_set))
        return final_list

    # TODO
    # override is_solved
    # this WordLadderPuzzle is solved when _from_word is the same as
    # _to_word

    def is_solved(self):
        """
        Return whether WordLadderPuzzle self is solved.

        @param self: WordLadderPuzzle
        @return: bool

        >>> puzzle = WordLadderPuzzle("computer", "computer", {"fun"})
        >>> puzzle.is_solved()
        True
        """
        return self._from_word == self._to_word

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
