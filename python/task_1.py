from pprint import pprint
import random
import math


TIMESTAMPS_COUNT = 50000

OFFSET_MAX_STEP = 3

# ##################################################################################
from typing import TypedDict

random.seed(11)


class SCORE_TYPE(TypedDict):
    home: int
    away: int


class INITIAL_STAMP_TYPE(TypedDict):
    offset: int
    score: SCORE_TYPE


class IncorrectOffsetValueError(Exception):
    """Exception raised for errors in the input offset.
    message -- explanation of the error
    """

    def __init__(self):
        self.message = f"Offset must be int type, more then 0 and less {TIMESTAMPS_COUNT * OFFSET_MAX_STEP:_}"
        super().__init__(self.message)


class GameStempsIncorrectError(Exception):
    """Exception raised for errors in the input game_stamps.
    message -- explanation of the error
    """

    def __init__(self):
        self.message = f"game_stamps must be list and len must be more 0"
        super().__init__(self.message)


# ##################################################################################

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45


INITIAL_STAMP: INITIAL_STAMP_TYPE = {"offset": 0, "score": {"home": 0, "away": 0}}


def generate_stamp(previous_value: INITIAL_STAMP_TYPE) -> INITIAL_STAMP_TYPE:
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = (
        1 if score_changed and random.random() > 1 - PROBABILITY_HOME_SCORE else 0
    )
    away_score_change = 1 if score_changed and not home_score_change else 0

    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change,
        },
    }


def generate_game() -> list[INITIAL_STAMP_TYPE]:
    stamps = [
        INITIAL_STAMP,
    ]

    current_stamp = INITIAL_STAMP

    for _ in range(TIMESTAMPS_COUNT):
        _new_stamp = generate_stamp(current_stamp)

        if current_stamp["score"] != _new_stamp["score"]:
            stamps.append(_new_stamp)

        current_stamp = _new_stamp

    return stamps


random.seed(11)


def get_score(game_stamps: list[INITIAL_STAMP_TYPE], offset: int):
    """
    Takes list of game's stamps and time offset for which returns the scores for the home and away teams.
    Please pay attention to that for some offsets the game_stamps list may not contain scores.
    """
    if (
        not isinstance(offset, int)
        or offset <= -1
        or offset > TIMESTAMPS_COUNT * OFFSET_MAX_STEP
    ):
        raise IncorrectOffsetValueError

    if len(game_stamps) == 0 or not isinstance(game_stamps, list):
        raise GameStempsIncorrectError

    last = game_stamps[0]

    for item in game_stamps:
        item_offset = item["offset"]
        if item_offset <= offset:
            last = item

    return [*last["score"].values()]


game_stamps = generate_game()

home, away = get_score(game_stamps, 100)
