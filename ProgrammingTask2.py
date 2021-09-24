import random


class InterfaceStrings:
    """ Class containing all the strings necessary for input """

    # sorry for using class but
    def __init__(self,
                 input_size_msg: str,
                 negative_size_msg: str,
                 even_size_msg: str,
                 wrong_size_format_msg: str,
                 input_matrix_msg: str,
                 mismatch_msg: str,
                 wrong_elem_format_msg: str,
                 input_range_msg: str,
                 wrong_range_format_msg: str,
                 previous_output_msg: str,
                 output_msg: str,
                 input_query_msg,
                 exit_msg: str,
                 wrong_query_msg: str,
                 choices_msg: str):
        """
        Initialization strings containing object for user interface

        :param input_size_msg: string message before size input
        :param wrong_size_format_msg: string message when size is incorrect type or format
        :param negative_size_msg: string message when size is non-positive
        :param even_size_msg: string message when size is even

        :param input_matrix_msg: string message before matrix input
        :param mismatch_msg: string message when matrix is mismatched
        :param wrong_elem_format_msg: string message when matrix element is incorrect

        :param input_range_msg: string message before range input
        :param wrong_range_format_msg: string message when range is incorrect

        :param previous_output_msg: string message for intermediate results
        :param output_msg: string message

        :param input_query_msg: string message
        :param exit_msg: string message
        :param wrong_query_msg: string message

        :param choices_msg: string message
        :return:
        """

        self.input_size = input_size_msg
        self.wrong_size_format = wrong_size_format_msg
        self.negative_size = negative_size_msg
        self.even_size = even_size_msg

        self.input_matrix = input_matrix_msg
        self.mismatch = mismatch_msg
        self.wrong_elem_format = wrong_elem_format_msg

        self.input_range = input_range_msg
        self.wrong_range_format = wrong_range_format_msg

        self.previous_output = previous_output_msg
        self.output = output_msg

        self.input_query = input_query_msg
        self.exit = exit_msg

        self.wrong_query = wrong_query_msg
        self.choices = choices_msg


class ImmediateExit(Exception):
    """ Class for force exit exception"""
    pass


class IncorrectData(Exception):
    """ Class for invalid data exception"""

    def __init__(self, msg):
        self.msg = msg


def validate_size(size, messages: InterfaceStrings):
    """
    Function managing all details about size input
    :param size: integer number to be checked
    :param messages: InterfaceStrings object for UI and convenience
    :return: same integer number if valid
    """

    if size <= 0:
        raise IncorrectData(messages.negative_size)

    elif size % 2 == 0:
        raise IncorrectData(messages.even_size)

    else:
        return size


def input_size(messages: InterfaceStrings):
    """
     Function managing all details about matrix size input process
    :param messages: InterfaceStrings object for UI and convenience
    :return: valid size value
    """

    print(messages.input_size)
    while True:
        size = input()
        try:
            number = validate_size(int(size), messages)

        except ValueError:
            print(messages.wrong_size_format)

        except IncorrectData as instance:
            print(instance.msg)

        else:
            return number


def input_range(messages: InterfaceStrings):
    """
    Function managing all details about range input process
    :param messages: InterfaceStrings object for UI and convenience
    :return: tuple of valid floats
    """

    print(messages.input_range)
    while True:
        try:
            a, b = input().split()
            a, b = float(a), float(b)

        except ValueError:
            print(messages.wrong_range_format)

        else:
            return a, b


def validate_matrix(matrix, size: int, messages: InterfaceStrings):
    """
    Returns a valid matrix if possible or exceptions
    :param matrix: pseudo-matrix of strings
    :param size:
    :param messages: InterfaceStrings object for UI and convenience
    :return: square float matrix if possible
    """

    # rows count validation
    if len(matrix) != size:
        raise IncorrectData(messages.mismatch)

    for row in range(size):
        if len(matrix[row]) != size:
            # elements in a row count validation
            raise IncorrectData(messages.mismatch)

        else:
            # converting strings into float if possible
            for elem in range(size):
                matrix[row][elem] = float(matrix[row][elem])

    # return valid matrix
    return matrix


def generate_random_square_matrix(size: int, least: float, largest: float, precision: int):
    """
    Function for random matrix generation
    :param size: matrix dimensions
    :param least: smallest value in the range
    :param largest: largest value in the range
    :param precision: precision of printing float
    :return: float square matrix of random values
    """

    # matrix prototype
    matrix = [[0.] * size for _ in range(size)]

    # generating random values in matrix
    for row in range(size):
        for elem in range(size):
            # entering row-by-row
            matrix[row][elem] = round(random.uniform(least, largest), precision)

    # returning ready matrix
    return matrix


def input_square_matrix(size: int, messages: InterfaceStrings):
    """
    Function managing input square matrix manually
    :param size: dimensions of matrix
    :param messages: InterfaceStrings object for UI and convenience
    :return: square float matrix
    """

    print(messages.input_matrix)
    while True:
        # matrix prototype
        matrix = [0] * size

        # elements input
        for row in range(size):
            matrix[row] = [elem for elem in input().split()]

        try:
            matrix = validate_matrix(matrix, size, messages)

        except ValueError:
            print(messages.wrong_elem_format)

        except IncorrectData as instance:
            print(instance.msg)

        else:
            return matrix


def find_largest_on_diagonals(matrix, size: int):
    """
    finds largest value on diagonals of some sub-matrix
    :param matrix: matrix of floats, ints or other comparable types
    :param size: size of sub-matrix
    :return: location of first largest element
    """

    # assume max value is first element
    max_value = matrix[0][0]
    i, j = 0, 0

    # finding maximum
    for k in range(size):
        # main diagonal
        if matrix[k][k] > max_value:
            max_value = matrix[k][k]
            i, j = k, k

        # side diagonal
        if matrix[k][size - 1 - k] > max_value:
            max_value = matrix[k][size - 1 - k]
            i, j = k, size - 1 - k

    return i, j


def swipe_elements_in_matrix(matrix, elem_1: tuple, elem_2: tuple):
    """
    Swipe two elements in given positions
    :param matrix: matrix to modify
    :param elem_1: first element location(two integers)
    :param elem_2: second element location(to integers)
    :return:
    """

    # swipe elements. IndexError raise is implicitly provided
    matrix[elem_1[0]][elem_1[1]], matrix[elem_2[0]][elem_2[1]] = \
        matrix[elem_2[0]][elem_2[1]], matrix[elem_1[0]][elem_1[1]]


def swap_diagonal_and_central(matrix):
    """
    Swaps the largest in-diagonal and central elements
    :param matrix: matrix to modify
    :return:
    """

    # no need to mention size explicitly
    size = len(matrix)

    # finding according element
    i, j = find_largest_on_diagonals(matrix, size)
    middle = size // 2

    # swipe them
    swipe_elements_in_matrix(matrix, (i, j), (middle, middle))


def print_matrix(msg: str, matrix, size):
    """
    Prints sub-matrix of floats with some precision
    :param msg: string message before matrix
    :param matrix: matrix to print
    :param size: size of sub-matrix to print
    :return:
    """

    print(msg)

    # printing matrix
    for row in range(size):
        print(*matrix[row], sep=' ')


def alternative_1(messages: InterfaceStrings):
    """
    Action set when user choose '1'
    :param messages: InterfaceStrings object for UI and convenience
    :return:
    """
    size = input_size(messages)
    matrix = input_square_matrix(size, messages)

    swap_diagonal_and_central(matrix)
    print_matrix(messages.output, matrix, size)


def alternative_2(messages: InterfaceStrings):
    """
    Action set when user choose '2'
    :param messages: InterfaceStrings object for UI and convenience
    :return:
    """
    # unimplemented possibility to generate floats of certain precision
    precision = 3

    size = input_size(messages)
    least, largest = input_range(messages)

    matrix = generate_random_square_matrix(size, least, largest, precision)
    print_matrix(messages.previous_output, matrix, size)

    swap_diagonal_and_central(matrix)
    print_matrix(messages.output, matrix, size)


def process_query(entry, messages: InterfaceStrings):
    """
    Function for processing query
    :param entry: query
    :param messages: InterfaceStrings object for UI and convenience
    :return:
    """

    if entry == "1":
        alternative_1(messages)

    elif entry == "2":
        alternative_2(messages)

    elif entry == "3":
        raise ImmediateExit

    else:
        print(messages.wrong_query)
        print(messages.choices)


def menu():
    """
    Initializes messages and returns InterfaceStrings object
    :return: InterfaceStrings object
    """
    choices_msg = "Виберіть одну з наступних дій для виконання:\n" \
                  "1. Ввести квадратну матрицю непарної розмірності власноруч\n" \
                  "2. Автоматично згенерувати матрицю непарної розмірності в заданому діапазоні\n" \
                  "3. Вийти з програми"

    input_size_msg = "Введіть розмір вашої квадратної матриці, яка є непарним числом"

    wrong_size_format_msg = "Ваше ціле число взагалі не того формату чи типу. Введіть ще раз"
    negative_size_msg = "Матриця даного розміру апріорі не може бути створена"
    even_size_msg = "Даний розмір не є непарним числом. Введіть будь-ласка непарне."

    input_matrix_msg = "Введіть матрицю власноруч. Вона відображатиметься саме так, як ви ввели"
    mismatch_msg = "Дана матриця не є коректної заявленої форми. Спробуйте ввести ще раз"
    wrong_elem_format_msg = "В вашій матриці є елементи некоректного типу або формату.\n" \
                            "Виправте це, будь-ласка!"

    input_range_msg = "Введіть два числа А і В, щоб згенерувати матрицю з чисел даного діапазону"
    wrong_range_format_msg = "Діапазон задано некоректним форматом або типом. Спробуйте ще раз"

    def input_query_msg(x):
        return f"[{x}]: "

    previous_output_msg = "Випадково згенерована матриця має такий вигляд: "
    output_msg = "Результат роботи основної функції такий: "

    exit_msg = "До побачення!"
    wrong_query_msg = "Запит невірний, введіть будь ласка правильно"

    return InterfaceStrings(input_size_msg,
                            negative_size_msg, even_size_msg, wrong_size_format_msg,
                            input_matrix_msg, mismatch_msg, wrong_elem_format_msg,
                            input_range_msg, wrong_range_format_msg,
                            previous_output_msg, output_msg,
                            input_query_msg, exit_msg, wrong_query_msg,
                            choices_msg)


def main():
    """
    Main code
    :return:
    """
    messages = menu()
    print(messages.choices)

    counter = 1
    while True:
        query = input(messages.input_query(counter))
        try:
            process_query(query, messages)
        except ImmediateExit:
            print(messages.exit)
            return
        except KeyboardInterrupt:
            print(messages.exit)
            return
        else:
            counter += 1


if __name__ == "__main__":
    main()
