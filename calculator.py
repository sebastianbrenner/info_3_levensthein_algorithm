class Calculator:

    def __init__(self, scrambledText, referenceText):
        assert scrambledText is not None and referenceText is not None
        self.__scrambledText = scrambledText
        self.__referenceText = referenceText
        self.__matrix = []

        # create matrix with the size of the parameter text length
        for y in range(0, len(scrambledText) + 1):
            self.__matrix.append([])
            for x in range(0, len(referenceText) + 1):
                self.__matrix[y].append(0)

        # fill matrix with start values
        # [DELETE MATRIX COMMENT]
        # 0  1  2  3
        # 1
        # 2
        # 3
        for x in range(0, len(referenceText) + 1):
            self.__matrix[0][x] = x
        for y in range(0, len(scrambledText) + 1):
            self.__matrix[y][0] = y

    def calcCost(self):
        """
            Calculates the matrix vaules.

            This calculates each value of the matrix using the Levensthein algorithm.

            :return: Matrix value in the bottom right (= Levensthein distance)
            :rtype: int
        """

        assert self.__matrix is not None

        for x in range(1, len(self.__scrambledText) + 1, 1):
            for y in range(1, len(self.__referenceText) + 1, 1):
                self.__matrix[x][y] = self.getMinimum(x, y)

        assert self.__matrix is not None

        return self.__matrix[len(self.__scrambledText)][len(self.__referenceText)]

    def getMinimum(self, row, col):
        """
            Calculates the minimum of a single cell.

            This method calls the replace, insert and delete methods with the given coordinates.
            Then returns the minimum return value.

            :param row: Row of the cell
            :param col: Coll of the cell
            :type row: int
            :type col: int
            :return: Minimum return value
            :rtype: int
        """

        assert row >= 0 and col >= 0

        m = min(self.replace(row, col), self.insert(row, col), self.delete(row, col))

        assert m is not None

        return m

    def c(self, row, col):
        """
            Calculates the c value.

            This method calculates the c value of a single cell after the this schema:
            c = 0, when s[i] = t[j], otherwise c = 1

            :param row: Row of the cell
            :param col: Coll of the cell
            :type row: int
            :type col: int
            :return: C value
            :rtype: int
        """
        assert row >= 0 and col >= 0

        if self.__scrambledText[row - 1] == self.__referenceText[col - 1]:
            return 0
        else:
            return 1

    def replace(self, row, col):
        """
            Calculates the replace value.

            This method calculates the replace value of a single cell after the this schema:
            M[i-1][j-1] + c

            :param row: Row of the cell
            :param col: Coll of the cell
            :type row: int
            :type col: int
            :return: Replace value
            :rtype: int
        """
        assert row >= 0 and col >= 0

        return self.__matrix[row - 1][col - 1] + self.c(row, col)

    def insert(self, row, col):
        """
            Calculates the insert value.

            This method calculates the insert value of a single cell after the this schema:
            M[i][j-1] + 1

            :param row: Row of the cell
            :param col: Coll of the cell
            :type row: int
            :type col: int
            :return: Insert value
            :rtype: int
        """
        assert row >= 0 and col >= 0

        return self.__matrix[row][col - 1] + 1

    def delete(self, row, col):
        """
            Calculates the delete value.

            This method calculates the delete value of a single cell after the this schema:
             M[i-1][j] + 1

            :param row: Row of the cell
            :param col: Coll of the cell
            :type row: int
            :type col: int
            :return: Delete value
            :rtype: int
        """
        assert row >= 0 and col >= 0

        return self.__matrix[row - 1][col] + 1

    def replaceName(self):
        """
            Calc if Levensthein Distance is equal or less than 25%.

            This returns true if the distance is equal or less than 25%, otherwise false.

            :return: Bool value
            :rtype: bool
        """
        return (self.calcCost() / len(self.__scrambledText)) <= 0.25

    @property
    def matrix(self):
        return self.__matrix

    @matrix.setter
    def matrix(self, matrix):
        self.__matrix = matrix

    @property
    def textcol(self):
        return self.__referenceText

    @textcol.setter
    def textcol(self, textcol):
        self.__referenceText = textcol

    @property
    def textrow(self):
        return self.__scrambledText

    @textrow.setter
    def textrow(self, textrow):
        self.__scrambledText = textrow

    def __str__(self):
        # custom string method
        s = ""
        for row in self.__matrix:
            for col in row:
                s += str(col) + "\t"
            s += "\n\n"
        return s
