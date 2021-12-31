from random import randint


class Grid:
    """
    Class for square grid filled with '-', 'X' and another unpredicted things
    """
    def __init__(self, size: int):
        self.size = size
        self.grid = [['-'] * size for _ in range(size)]

        # set is required for unique values of random spots
        self.spots = set()

    def __str__(self):
        result_string = ''
        for line in self.grid:
            result_string += " ".join(line) + '\n'
        return result_string

    def _generate_spot(self):
        return randint(0, self.size - 1), randint(0, self.size - 1)

    def clear(self):
        """
        Clear entire grid
        """
        for (x, y) in self.spots:
            self.grid[x][y] = '-'
        self.spots.clear()

    def randomize_spots(self, spots: int):
        """
        Occupy according number of cells
        """
        if spots > self.size ** 2:
            raise ValueError("Impossible to fit more spots than available cells")

        if self.spots:
            self.clear()

        # loop while required for cells uniqueness
        successfully_generated = 0
        while successfully_generated < spots:
            x, y = self._generate_spot()
            if (x, y) not in self.spots:
                self.spots.add((x, y))
                self.grid[x][y] = 'X'
                successfully_generated += 1


class Solution(Grid):
    """
    Dynamic programming solution class for task
    Idea: create another 'grid' that counts
    The largest size for square that ends in this cell
    """

    def __init__(self, size):
        super().__init__(size)
        self.squares_grid = [[0] * size for _ in range(size)]

        self.maximum = None
        self.location_of_maximum = None

    def calculate_squares(self):
        """
        Main algorithm: counting values of auxiliary matrix
        Idea: expand the square by left, upper or left-upper neighbour
        """
        # loop 1: 'squares' of first row and column
        for i in range(self.size):
            if self.grid[0][i] == '-':
                self.squares_grid[0][i] = 1

                if self.maximum is None:
                    self.maximum = 1
                    self.location_of_maximum = (0, i)

            if self.grid[i][0] == '-':
                self.squares_grid[i][0] = 1

                if self.maximum is None:
                    self.maximum = 1
                    self.location_of_maximum = (i, 0)
        else:
            if self.maximum is None:
                self.maximum = 0
                self.location_of_maximum = (0, 0)

        # loop 2 (the ugliest but important part): count the size of square for each cell
        # And seek maximum square
        for i in range(1, self.size):
            for j in range(1, self.size):
                if self.grid[i][j] == '-':
                    self.squares_grid[i][j] = 1 + min(self.squares_grid[i][j - 1],
                                                      self.squares_grid[i - 1][j],
                                                      self.squares_grid[i - 1][j - 1])

                    if self.maximum < self.squares_grid[i][j]:
                        self.maximum = self.squares_grid[i][j]
                        self.location_of_maximum = (i, j)

    def embed_maximal_square(self):
        """
        Embed the largest square found by preceding algorithm
        """
        h = self.maximum
        x, y = self.location_of_maximum

        for i in range(x, x - h, -1):
            for j in range(y, y - h, -1):
                self.grid[i][j] = 's'

    @property
    def max_square_size(self):
        return self.maximum


class Program:
    """
    Functor class for main program
    """
    def __init__(self):
        pass

    @staticmethod
    def __call__(*args, **kwargs):
        count = input("Enter the count of occupied cells: ")
        if not count.isnumeric():
            print("Invalid format or number")

        else:
            solution_grid = Solution(10)
            try:
                solution_grid.randomize_spots(int(count))

            except ValueError as error:
                print(error)

            else:
                solution_grid.calculate_squares()
                solution_grid.embed_maximal_square()
                print(solution_grid)
                print("The size of square side is", solution_grid.max_square_size)


if __name__ == "__main__":
    Program()()
