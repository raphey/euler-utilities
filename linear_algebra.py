__author__ = 'raphey'


class Matrix(object):
    def __init__(self, values, update_function=lambda x: x):
        """
        :param values: List of list containing matrix values
        :param update_function: Function to be applied elementwise whenever matrix is created (e.g. modulo or rounding)
        """
        self.values = values
        self.shape = len(values), len(values[0])
        self.height, self.width = self.shape
        self.update_function = update_function
        self.update_elements()

    def __copy__(self):
        new_values = [row.copy() for row in self.values]
        return Matrix(new_values, self.update_function)

    def __mul__(self, other):
        if type(other) is Vector:
            return self.multiply_by_vector(other)
        if self.width != other.height:
            raise ValueError('Matrix dimensions don\'t match: {} and {}'.format(self.shape, other.shape))
        return Matrix(self.matrix_multiply_backend(self.values, other.values), self.update_function)

    def __pow__(self, power):
        a = self.__copy__()
        result = self.get_identity_matrix()
        while power > 0:
            if power % 2 == 1:
                result *= a
            a *= a
            power //= 2
        return result

    def __str__(self):
        return '[' + '\n '.join('\t'.join(map(str, row)) for row in self.values) + ']'

    def multiply_by_vector(self, other):
        product_as_matrix = self * Matrix(other.values)
        return Vector([x[0] for x in product_as_matrix.values])

    @staticmethod
    def matrix_multiply_backend(a, b):
        new_height, new_width = len(a), len(b[0])
        shared_dimension = len(a[0])
        product = [[0] * new_width for _ in range(new_height)]
        for i in range(new_height):
            for j in range(new_width):
                for k in range(shared_dimension):
                    product[i][j] += a[i][k] * b[k][j]
        return product

    def get_identity_matrix(self):
        if self.height != self.width:
            raise ValueError('Trying to make identity matrix with unequal dimensions: {}'.format(self.shape))
        n = self.width
        identity_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            identity_matrix[i][i] = 1
        return Matrix(identity_matrix, self.update_function)

    def update_elements(self):
        for i in range(self.height):
            for j in range(self.width):
                self.values[i][j] = self.update_function(self.values[i][j])

    def v_stack(self, other):
        if self.width != other.width:
            raise ValueError('Matrices have unequal widths: {}, {}'.format(self.width, other.width))
        return Matrix(self.values + other.values, self.update_function)

    def h_stack(self, other):
        if self.height != other.height:
            raise ValueError('Matrices have unequal heights: {}, {}'.format(self.height, other.height))
        return Matrix([self.values[i] + other.values[i] for i in range(self.height)])


class Vector(object):
    def __init__(self, value_list):
        # Vectors are essentially n by 1 matrices under the hood
        self.values = [[x] for x in value_list]
        self.length = len(value_list)

    def __str__(self):
        return '[' + '\t'.join(map(str, [x[0] for x in self.values])) + ']'


class ModMatrix(Matrix):
    def __init__(self, values, m):
        super(ModMatrix, self).__init__(values, update_function=lambda x: x % m)
