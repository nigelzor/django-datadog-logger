import unittest
import threading
import time

from django_datadog_logger.recursion import not_recursive, RecursionDetected


class TestNotRecursiveDecorator(unittest.TestCase):
    def test_blocks_simple_recursion(self):
        @not_recursive
        def recursive_func():
            return recursive_func()

        with self.assertRaises(RecursionDetected):
            recursive_func()

    def test_allows_sequential_calls(self):
        @not_recursive
        def normal_func(x):
            return x * 2

        self.assertEqual(normal_func(5), 10)
        self.assertEqual(normal_func(10), 20)

    def test_thread_isolation(self):
        results = []

        @not_recursive
        def slow_func():
            time.sleep(0.1)
            results.append(True)

        # Run the function in two separate threads simultaneously
        t1 = threading.Thread(target=slow_func)
        t2 = threading.Thread(target=slow_func)

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Both threads should have finished successfully
        self.assertEqual(len(results), 2)
