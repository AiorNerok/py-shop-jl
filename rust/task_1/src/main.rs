use rand::Rng;

const TIMESTAMPS_COUNT: usize = 50000;

const PROBABILITY_SCORE_CHANGED: f64 = 0.0001;

const PROBABILITY_HOME_SCORE: f64 = 0.45;

const OFFSET_MAX_STEP: i32 = 3;

const INITIAL_STAMP: Stamp = Stamp {
    offset: 0,
    score: Score { home: 0, away: 0 },
};

#[derive(Debug, Clone, Copy, PartialEq)]
struct Score {
    home: i32,
    away: i32,
}

impl Score {
    fn values(&self) -> (i32, i32) {
        (self.home, self.away)
    }
}

#[derive(Debug, Clone, Copy)]
struct Stamp {
    offset: i32,
    score: Score,
}

fn generate_stamp(previous_value: Stamp) -> Stamp {
    let score_changed: bool = rand::thread_rng().gen_bool(PROBABILITY_SCORE_CHANGED);
    let home_score_change: bool = rand::thread_rng().gen_bool(PROBABILITY_HOME_SCORE);
    let offset_change: i32 = rand::thread_rng().gen_range(1..=OFFSET_MAX_STEP);

    Stamp {
        offset: previous_value.offset + offset_change,
        score: Score {
            home: previous_value.score.home
                + if score_changed && home_score_change {
                    1
                } else {
                    0
                },
            away: previous_value.score.away
                + if score_changed && !home_score_change {
                    1
                } else {
                    0
                },
        },
    }
}

fn generate_game() -> Vec<Stamp> {
    let mut stamps = vec![INITIAL_STAMP];
    let mut current_stamp = INITIAL_STAMP;

    for _ in 0..TIMESTAMPS_COUNT {
        let result = generate_stamp(current_stamp);
        if result.score != current_stamp.score {
            stamps.push(result);
        }

        current_stamp = result
    }

    stamps
}

fn get_score(game_stamps: &[Stamp], offset: i32) -> (i32, i32) {
    let mut local = INITIAL_STAMP;

    for item in game_stamps {
        if offset < item.offset {
            break;
        }

        local = item.clone();
    }

    local.score.values()
}

fn main() {
    let stamps = generate_game();
    let result = get_score(&stamps, 40000);
    println!("{:#?}", result);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_score_initial_offset() {
        let stamps = vec![INITIAL_STAMP];
        let result = get_score(&stamps, 0);
        assert_eq!(result, (0, 0));
    }

    #[test]
    fn test_get_score_end_offset() {
        let stamps = generate_game();
        let result = get_score(&stamps, 50000);
        let final_score = stamps.last().unwrap().score.values();
        assert_ne!(result, final_score);
    }

    #[test]
    fn test_get_score_offset_out_of_range() {
        let stamps = generate_game();
        let result = get_score(&stamps, 100000);
        let final_score = stamps.last().unwrap().score.values();
        assert_eq!(result, final_score);
    }

    #[test]
    fn test_get_score_empty_stamps() {
        let stamps: Vec<Stamp> = vec![];
        let result = get_score(&stamps, 0);
        assert_eq!(result, (0, 0));
    }
}
