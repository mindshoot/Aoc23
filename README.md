# Aoc23
[Advent of Code '23](https://adventofcode.com/2023)

> NB: spoilers below

## Day 1

Part 2 was pretty tricky: the sample data left it a big ambiguous about how to handle overlapping words, 
eg should the numbers from `twone3` be `23`, `213`, `13` or something else.

<details>
  <summary>Spoiler</summary>
  
  My initial guess was wrong - overlapping words are all counted.
</details>

## Day 2

Much more straightforward today. 

## Day 3

Now I know how to get a rolling window of three items in an array. Thank you `itertools`

## Day 4

Short and sweet

## Day 5

Nightmare!

## Day 6

Luckily used the maths approach for the first half, which saved effort

## Day 7

Quite fiddly, but also quite fun, so ...

## Day 8

Part 1 was deceptively easy. Part 2 was not going to succumb to brute force, 
so other options were needed. This was the first one that felt like it needed
some exploration and tyre-kicking to get the lay of the land to have a chance
of solving.

## Day 9

Like a refreshing palette-cleanser after the heavy meal that was day 8. Did it
while the coffee machine was warming up. Part 2 thankfully not a nightmare.

## Day 10

I found the second part realllly hard. 

## Day 11

A bit fiddly, but much more tractable than yesterday!

## Day 12

I thought I'd be dropping a star today. The first part wasn't too bad, but I
feared the second bit was like day 8 and would require a different approach
though. Thankfully, a flash of insight (and the use of `functools.cache`) meant
the day was saved.
