import unittest

import numpy as np

from evaluation.simulation import Taxi, AVG_SPEED, euclidean_distance


class TestTaxi(unittest.TestCase):
    def test_go_simple(self):
        entries = [(5, (0.0, 0.0), 10, (3.0, 4.0))]

        taxi = Taxi(0, (0.0, 0.0))

        for pickup_time, pickup_loc, drop_time, drop_loc in entries:
            taxi.schedule_go(pickup_time, pickup_loc, drop_time, drop_loc)
            taxi.advance_time(drop_time)

        self.assertEqual(taxi.total_distance, 5.0)

    def test_go_multiple(self):
        entries = [(5, (0.0, 0.0), 10, (3.0, 4.0)),
                   (15, (6.0, 8.0), 20, (3.0, 4.0))]

        taxi = Taxi(0, (0.0, 0.0))

        for pickup_time, pickup_loc, drop_time, drop_loc in entries:
            taxi.schedule_go(pickup_time, pickup_loc, drop_time, drop_loc)
            taxi.advance_time(drop_time)

        self.assertEqual(taxi.total_distance, 15.0)

    def test_sim_then_go(self):
        start_pos = (0.0, 0.0)
        taxi = Taxi(0, start_pos)

        initial_destination = (5.0, 5.0)
        taxi.schedule_go_sim(initial_destination)

        pickup_time = 2
        pickup_loc = (5.0, 0.0)
        drop_time = 5
        drop_loc = (5.0, 5.0)

        taxi.schedule_go(pickup_time, pickup_loc, drop_time, drop_loc)

        self.assertEqual(taxi.total_distance, 0)  # We have not advanced time yet

        taxi.advance_time(1)

        # Since we move for 1 seconds, we expect to be at 0.0 + 1*AVG_SPEED for both coordinates. (Target: 5, 5)
        mul = np.cos(45.0 * np.pi / 180.0)
        middle_pos = (AVG_SPEED * mul, AVG_SPEED * mul)
        expected_unpaid_distance = euclidean_distance(start_pos, middle_pos)
        self.assertAlmostEqual(taxi.total_distance, expected_unpaid_distance)

        # Advance again to t=2
        taxi.advance_time(2)

        # Since we move for 2 seconds, we expect to be at 0.0 + 2*AVG_SPEED for both coordinates. (Target: 5, 5)
        # Then from there, we move to (5, 0) and then back to (5, 5).
        middle_pos2 = (2 * AVG_SPEED * mul, 2 * AVG_SPEED * mul)
        expected_unpaid_distance += euclidean_distance(middle_pos, middle_pos2) + \
                                    euclidean_distance(middle_pos2, pickup_loc)
        expected_paid_distance = euclidean_distance(pickup_loc, drop_loc)

        self.assertAlmostEqual(taxi.total_distance, expected_paid_distance + expected_unpaid_distance)
        self.assertAlmostEqual(taxi.total_paid_distance, expected_paid_distance)

        # No tasks should be left, advance time and check
        taxi.advance_time(3)

        self.assertAlmostEqual(taxi.total_distance, expected_paid_distance + expected_unpaid_distance)
        self.assertAlmostEqual(taxi.total_paid_distance, expected_paid_distance)


if __name__ == '__main__':
    unittest.main()
