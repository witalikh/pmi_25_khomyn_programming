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
    if len(iterable) <= 1:
        return iterable

    else:
        pivot = iterable[len(iterable) // 2]

        cls = type(iterable)
        lesser, equal, greater = cls(), cls(), cls()

        for element in iterable:
            # print(type(key(element)), key(element))
            # print(type(key(pivot)), key(pivot))
            if key(element) < key(pivot):
                lesser.append(element)
            elif key(element) == key(pivot):
                equal.append(element)
            else:
                greater.append(element)

        if reverse:
            return quick_sort(greater, reverse, key) + \
                   equal + \
                   quick_sort(lesser, reverse, key)

        else:
            return quick_sort(lesser, reverse, key) + \
                   equal + \
                   quick_sort(greater, reverse, key)
