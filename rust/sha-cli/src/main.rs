use clap::{Arg, Command};
use sha256::digest;
use std::thread;
use std::time::{Duration, Instant};

fn main() {
    let m = Command::new("cli")
        .arg(
            Arg::new("N")
                .short('N')
                .required(true)
                .help("ends with N-zero characters"),
        )
        .arg(
            Arg::new("F")
                .short('F')
                .required(true)
                .help("how many hash values ​​to find"),
        )
        .get_matches();

    let n = m.get_one::<String>("N").unwrap().to_owned();

    let f = m.get_one::<String>("F").unwrap().to_owned();

    let start = Instant::now();

    // let handle = thread::spawn(move || {
        let mut count_find: usize = 0;
        let mut count_iter: usize = 1;
        let n = n.parse::<u8>().unwrap();
        let f = f.parse::<u8>().unwrap().into();

        let end_str = "0".repeat(n.into());

        loop {
            let res = digest(count_iter.to_string());

            if res.ends_with(&end_str) {
                println!("{}, {}", count_iter, res);
                count_find += 1
            }

            if count_find == f {
                break;
            }
            count_iter += 1;
        }
    // });
    // handle.join().unwrap();

    let duration = start.elapsed();
    println!("Time elapsed in expensive_function() is: {:?}", duration);
}
