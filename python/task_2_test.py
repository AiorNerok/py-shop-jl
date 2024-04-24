import unittest
import random

from task_1 import (
    get_score,
    generate_game,
    IncorrectOffsetValueError,
    GameStempsIncorrectError,
    TIMESTAMPS_COUNT,
    OFFSET_MAX_STEP,
)


class TestGetScore(unittest.TestCase):
    def setUp(self) -> None:
        random.seed(11)

        self.game_stamps = generate_game()
        self.get_score = get_score
        self.max_offset_value = TIMESTAMPS_COUNT * OFFSET_MAX_STEP

    def test_offset_equal_0(self):
        home, away = get_score(self.game_stamps, 0)
        self.assertEqual(home, 0)
        self.assertEqual(away, 0)

    def test_offset_equal_50000(self):
        home, away = get_score(self.game_stamps, 50000)
        self.assertEqual((home, away), (1, 1))

    def test_offset_equal_100000(self):
        home, away = get_score(self.game_stamps, 100000)
        self.assertTupleEqual((home, away), (1, 4))

    def test_offset_more_max_offset_value(self):
        self.assertRaises(
            IncorrectOffsetValueError,
            lambda: get_score(self.game_stamps, self.max_offset_value + 1),
        )

    def test_offset_less_0(self):
        self.assertRaises(
            IncorrectOffsetValueError, lambda: get_score(self.game_stamps, -1)
        )

    def test_offset_other_than_type_int(self):
        self.assertRaises(
            IncorrectOffsetValueError, lambda: get_score(self.game_stamps, [])
        )
        self.assertRaises(
            IncorrectOffsetValueError, lambda: get_score(self.game_stamps, "str")
        )
        self.assertRaises(
            IncorrectOffsetValueError, lambda: get_score(self.game_stamps, tuple())
        )

    def test_game_stamps_empty(self):
        self.assertRaises(GameStempsIncorrectError, lambda: get_score([], 100))


if __name__ == "__main__":
    unittest.main()
