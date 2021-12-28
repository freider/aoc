use std::env;
use regex::Regex;
use std::fs;

fn main() {
    let data = aoclib::aoc_input();
    part1(&data);
    part2(&data);
}

trait SimpleRe {
    fn capture_vec<'a>(&self, text: &'a str) -> Vec<&'a str>;
}

impl SimpleRe for Regex {
    fn capture_vec<'a>(&self, text: &'a str) -> Vec<&'a str> {
        self.captures(text).unwrap()
            .iter().skip(1)
            .flat_map(|c| c.map(|m| m.as_str()).or(Some("")))
            .collect()
    }
}

fn part1(data: &str) {
    let re = Regex::new(r"(\d+)-(\d+) (\w): (\w+)").unwrap();
    let ans = data.split("\n")
        .filter(|&l| {
            let caps = re.capture_vec(l);
            if let [lowstr, highstr, c, pw] = caps[..] {
                let cnt = pw.chars().filter(|d| *d == c.chars().next().unwrap()).count();
                let low: usize = lowstr.parse().unwrap();
                let high: usize = highstr.parse().unwrap();
                return low <= cnt && cnt <= high
            }
            false
        })
        .count();
    println!("{}", ans)
}

fn part2(data: &str) {
    let re = Regex::new(r"(\d+)-(\d+) (\w): (\w+)").unwrap();
    let ans = data.split("\n")
        .filter(|&l| {
            let caps = re.capture_vec(l);
            if let [lowstr, highstr, c, pw] = caps[..] {
                let low= lowstr.parse::<usize>().unwrap() - 1;
                let high = highstr.parse::<usize>().unwrap() - 1;
                return (&pw[low..low+1] == c) != (&pw[high..high+1] == c)
            }
            false
        })
        .count();
    println!("{}", ans)
}
