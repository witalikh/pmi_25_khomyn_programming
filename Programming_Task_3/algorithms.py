"""
File containing separately implemented
common class-independent algorithms
"""


def quick_sort(iterable, reverse=False, key=lambda x: x):
    """
    Out-place quicksort algorithm function
    :param iterable: iterable to be sorted
    :param reverse: reverse sorting order demand
    :param key: element converter into comparable value
    :return: sorted iterable
    """
    # nothing to sort
    if len(iterable) <= 1:
        return iterable

    # split iterable by pivot
    else:
        pivot = iterable[len(iterable) // 2]

        # universal iterable constructors
        cls = type(iterable)

        lesser = cls.__new__(cls)
        equal = cls.__new__(cls)
        greater = cls.__new__(cls)

        lesser.__init__()
        equal.__init__()
        greater.__init__()

        # TypeError can be raised if keys are incomparable
        for element in iterable:
            if key(element) < key(pivot):
                lesser.append(element)
            elif key(element) == key(pivot):
                equal.append(element)
            else:
                greater.append(element)

        # sort sub-iterables and return sorted
        if reverse:
            return quick_sort(greater, reverse, key) + \
                   equal + \
                   quick_sort(lesser, reverse, key)
        else:
            return quick_sort(lesser, reverse, key) + \
                   equal + \
                   quick_sort(greater, reverse, key)
