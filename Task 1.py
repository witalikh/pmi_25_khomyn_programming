class ImmediateExit(Exception):
    """ Custom exception for immediate program break """
    pass


def quick_sort(arr: list):
    """
    Quicksort algorithm implementation
    :param arr: list to be sorted (stays immutable)
    :return: sorted list
    """

    length = len(arr)

    # nothing to sort
    if length <= 1:
        return arr

    # split list by pivot
    else:
        pivot = arr[length // 2]
        lesser, equal, greater = [], [], []

        # TypeError can be raised if elements are incomparable
        for i in range(length):
            if arr[i] < pivot:
                lesser.append(arr[i])
            elif arr[i] == pivot:
                equal.append(arr[i])
            else:
                greater.append(arr[i])

        # sort sub-lists and return sorted
        return quick_sort(lesser) + equal + quick_sort(greater)


# main code of this task
# complexity in average is O(n*log(n) + n)
def count_unique(arr: list) -> int:
    """
    Counting unique elements
    """

    # if arr is empty
    if not arr:
        return 0
    else:
        # sorting arr
        sorted_arr = quick_sort(arr)

        # first element is already unique
        counter = 1

        # comparing current slot with previous to find uniques
        for i in range(1, len(sorted_arr)):
            if sorted_arr[i - 1] != sorted_arr[i]:
                counter += 1

        return counter


def try_to_input(required_type,
                 entry_msg, wrong_entry_msg,
                 stop_words):
    """
    Function that handles perpetual input until entering correct format
    """
    while True:
        # enter a value
        entry = input(entry_msg)

        # if we decide to close program beforehand
        if entry.lower() in stop_words:
            raise ImmediateExit

        try:
            # try to convert
            output = required_type(entry)

        except ValueError:
            # wrong format -> ask to rewrite
            print(wrong_entry_msg)
            continue

        else:
            # right format -> return
            return output


def list_input_manage(greeting_msg,
                      size_input_msg, elem_input_msg,
                      wrong_size_value_msg,
                      wrong_size_format_msg, wrong_elem_format_msg,
                      stop_words):
    """
    Function that handles array(list) input and returns formatted list
    """

    # greeting message
    print(greeting_msg)

    # getting list size
    size = try_to_input(int, size_input_msg, wrong_size_format_msg, stop_words)

    if size < 0:
        print(wrong_size_value_msg)
        raise ImmediateExit

    else:
        arr = []

        print(elem_input_msg)
        for i in range(size):
            counter_msg = f"[{i + 1}]: "
            arr.append(try_to_input(float, counter_msg, wrong_elem_format_msg, stop_words))

        return arr


def main():
    """ Main function of the program """

    greeting_msg = """
    Ця програма рахує кількість унікальних значень у вхідній послідовності
    Зокрема, для вхідної послідовності [3.14, -4.5, 3.3, 3.3, 3.14, 4]
    така кількість дорівнюватиме 4
    Щоб вийти передчасно, введіть EXIT в довільному регістрі.
    """

    size_input_msg = """
    Введіть кількість елементів у послідовності (ціле число)
    """

    elem_input_msg = """
    Введіть послідовність дійсних значень ПОЕЛЕМЕНТНО через ENTER                     
    Будь-ласка, введіть ціле число або EXIT (в довільному регістрі) щоб вийти.
    """

    wrong_size_value_msg = """
    Введене Вами число чисто технічно є цілим числом, однак масивів такого розміру,
    на жаль, ми ще не навчились підтримувати :)
    """

    wrong_size_input_msg = """
    Введено некоректний формат для розміру масиву. 
    Будь-ласка, введіть ціле число або EXIT (в довільному регістрі) щоб вийти.
    """

    wrong_elem_input_msg = """
    Введено некоректний формат для розміру масиву. 
    Будь-ласка, введіть ціле або дійсне число, або EXIT (в довільному регістрі) щоб вийти.
    """

    output_msg = "В даному вхідному масиві виявлено таку кількість унікальних елементів: "

    exit_msg = """
    Програма завершує свою роботу. Дякую за увагу!
    """

    stop_words = ["exit"]

    try:
        # obtaining array with function
        arr = list_input_manage(greeting_msg,
                                size_input_msg, elem_input_msg,
                                wrong_size_value_msg,
                                wrong_size_input_msg, wrong_elem_input_msg,
                                stop_words)

    except ImmediateExit:
        # user wants go out, let him free
        print(exit_msg)

    else:
        # printing results
        print(output_msg, count_unique(arr))


if __name__ == "__main__":
    main()
