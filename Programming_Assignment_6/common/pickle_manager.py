"""
File containing convenient functions for working with pickle files
"""
import pickle


def dump_all(filename, iterable):
    """
    Dumps all objects from iterable into pickle-file
    :param filename: path to file to dump contents
    :param iterable: iterable of objects to dump
    """
    with open(filename, 'wb') as file:
        pickle.dump(len(iterable), file)

        for element in iterable:
            pickle.dump(element, file)


def load_all(filename, type_cast=dict):
    """
    Load iterable of objects from pickle file
    :param filename: path to file to load from
    :param type_cast: type of objects to store in container
    :return:container of objects
    """
    result = []

    with open(filename, 'rb') as file:
        size = pickle.load(file)

        for _ in range(size):
            result.append(type_cast(**pickle.load(file)))

    return result
