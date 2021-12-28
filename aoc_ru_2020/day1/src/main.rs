use std::fs;
use itertools::Itertools;

fn solve(nums: &Vec<i32>, k: usize) -> i32 {
    let answer: i32 = nums.iter().combinations(k)
        .filter(|v| v.iter().map(|&x| x).sum::<i32>() == 2020)
        .map(|v| v.iter().fold(1, |x, y| x * (*y)))
        .next().unwrap();
    answer
}


fn main() {
    let contents = fs::read_to_string("inputs/1")
        .expect("Something went wrong reading the file");
    let nums: Vec<i32> = contents.split("\n").map(|x| x.parse::<i32>().unwrap()).collect();

    println!("{}", solve(&nums, 2));
    println!("{}", solve(&nums, 3));
}
