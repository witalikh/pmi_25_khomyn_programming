from unit_testing.assistant import *
from Memento import CareTaker, NothingToUndo, NothingToRedo


class MementoTests(TestCase):
    """ Namespace for memento tests """

    def test_real_undo_redo(self):
        """ Test: it should cancel and then return changes """

        sample_obj = {"key_1": "value_1", "key_2": "value_2"}

        container = []
        caretaker = CareTaker("unit_tests", container, dict)

        caretaker.snapshot_before_change()
        container.append(sample_obj)
        caretaker.accept_change()

        caretaker.undo()
        self.assertTrue(len(container) == 0)

        caretaker.redo()
        self.assertTrue(len(container) == 1)

        self.assertEqual(container[0], sample_obj)

    def test_fake_undo_redo(self):
        """ Test: it should cancel and then return changes """

        container = []
        caretaker = CareTaker("unit_tests", container, dict)

        caretaker.snapshot_before_change()
        caretaker.decline_change()

        self.assertRaises(NothingToUndo, caretaker.undo)
        self.assertRaises(NothingToRedo, caretaker.redo)

    def test_stack(self):
        """ Test: measure stack and with limited stack check if not exceeds """

        sample_obj = {"key_1": "value_1", "key_2": "value_2"}

        container = []
        caretaker = CareTaker("unit_tests", container, dict)
        caretaker.max_undo_actions = 2

        def action(method, *args):

            caretaker.snapshot_before_change()
            getattr(container, method)(*args)
            caretaker.accept_change()

        action("append", sample_obj)
        action("pop")
        action("append", sample_obj)

        def check_measure(list_size, undo_stack, redo_stack):

            self.assertEqual(len(container), list_size)
            self.assertEqual(caretaker.undo_count, undo_stack)
            self.assertEqual(caretaker.redo_count, redo_stack)

        check_measure(1, 2, 0)

        caretaker.undo()
        check_measure(0, 1, 1)

        action("append", sample_obj)
        check_measure(1, 2, 0)


__all__ = ["MementoTests"]
