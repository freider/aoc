use std::{env, fs};
use regex::Regex;

pub fn aoc_input() -> String {
    let main = env::args().next().unwrap();
    let res = Regex::new(r"day(\d+)").unwrap().captures(&main);
    let filename = format!("inputs/{}", &res.unwrap()[1]);
    let data = fs::read_to_string(filename).unwrap();
    data
}


#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
