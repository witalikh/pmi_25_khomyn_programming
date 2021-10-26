import os
import Common.pickle_manager as pickle_func
from settings import Globals


class NothingToUndo(Exception):
    pass


class NothingToRedo(Exception):
    pass


class Memento:
    """
    Class containing a state of Originator object
    """

    def __init__(self, state, obj):
        """
        Init memento object
        :param state: originator's current state
        :param obj: originator's current container
        """
        self.state = state
        self.filename = fr'snapshots\{state}.pickle'

        # make folder "snapshots" is doesnt exist
        if not os.path.exists("snapshots"):
            os.makedirs("snapshots")

        # dump container records in pickle file
        pickle_func.dump_all(self.filename, obj)

    def __del__(self):
        """
        Dunder method, called when memento is deleted
        """
        # remove file connected to this memento
        if os.path.isfile(self.filename):
            os.remove(self.filename)


class Originator:
    """
    The object of application that will state the changes
    """

    def __init__(self, obj, type_cast):
        """
        Init Originator object
        :param obj: object-iterable to observe for changes
        :param type_cast: type of objects inside container
        """

        # declared as private
        self._state = 0
        self._iterable = obj
        self._type = type_cast

    @property
    def state(self):
        """
        Getter of state of originator
        :return: non-assignable state of originator
        """
        return self._state

    def get_memento(self):
        """
        Create memento from current state of originator
        :return: memento object of current originator state
        """
        memento = Memento(self._state, self._iterable)
        self._state += 1
        return memento

    def set_memento(self, memento):
        """
        Establish memento to recover previous state
        :param memento: memento object to recover previous state
        """
        self._state = memento.state

        self._iterable.clear()
        self._iterable.extend(pickle_func.load_all(memento.filename, self._type))


class CareTaker:
    """
    Interface class for handling interaction of Mementos and Originator
    """

    max_undo_actions = Globals.max_undo_actions

    def __init__(self, obj, type_cast):
        """
        Initialize CareTaker object for container
        :param obj: iterable to be observed for changes
        :param type_cast: type of objects inside iterable
        """
        self._originator = Originator(obj, type_cast)

        # fake alert prevention
        self.pending = []

        # sequences ("stacks") for undo and redo
        self._undo_mementos = []
        self._redo_mementos = []

    def snapshot_before_change(self):
        """
        Snapshot memento of current state and wait if alert wasn't fake
        """
        memento = self._originator.get_memento()
        self.pending.append(memento)

    def accept_change(self):
        """
        Changes happened with object, so memo state for undo
        """
        memento = self.pending.pop()

        self._undo_mementos.append(memento)
        self._redo_mementos.clear()

        if CareTaker.max_undo_actions is not None and \
           len(self._undo_mementos) == CareTaker.max_undo_actions + 1:
            self._undo_mementos.pop(0)

    def decline_change(self):
        """
        No changes happened, don't memorize memento
        """
        last_version = self.pending.pop()
        self._originator.set_memento(last_version)

    def undo(self):
        """
        Undo option implementation
        """
        if len(self._undo_mementos) > 0:

            prev_memento: Memento = self._originator.get_memento()
            curr_memento: Memento = self._undo_mementos.pop()

            self._redo_mementos.append(prev_memento)
            self._originator.set_memento(curr_memento)

        else:
            raise NothingToUndo

    def redo(self):
        """
        Redo option implementation
        """
        if len(self._redo_mementos) > 0:

            prev_memento: Memento = self._originator.get_memento()
            curr_memento: Memento = self._redo_mementos.pop()

            self._undo_mementos.append(prev_memento)
            self._originator.set_memento(curr_memento)

        else:
            raise NothingToRedo

    @property
    def undo_count(self):
        """
        :return: count of undo mementos in stack
        """
        return len(self._undo_mementos)

    @property
    def redo_count(self):
        """
        :return: count of redo mementos in stack
        """
        return len(self._redo_mementos)
