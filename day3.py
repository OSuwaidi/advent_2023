# بسم الله الرحمن الرحيم وبه نستعين

"""
The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""
from rich import print

SYMBOLS = frozenset({
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+",
    "[", "]", "{", "}", "\\", "|", ";", ":", "'", "\"", ",", "<", ">",
    "/", "?", "~", "`"
})  # set lookup is O(1)


def sum_adj_nums(line: str, top_line: str | None, bottom_line: str | None) -> int:
    sum_nums = 0
    end_index = 0

    while end_index < max_chars:

        if line[end_index].isdigit():
            start_index = end_index

            while end_index + 1 < max_chars and line[end_index + 1].isdigit():
                end_index += 1

            number = int(line[start_index: end_index + 1])

            if start_index - 1 > 0:  # if the number is not in the beginning of the line:
                offset = 1
                adj_left: bool = line[start_index - offset] in SYMBOLS
                adj_right: bool = line[end_index + 1] in SYMBOLS if end_index + 1 < max_chars else False

            else:
                offset = 0
                adj_left = False
                adj_right = line[end_index + 1] in SYMBOLS

            adj_top = any(char in SYMBOLS for char in top_line[start_index - offset: end_index + 2]) if top_line else False

            adj_bot = any(char in SYMBOLS for char in bottom_line[start_index - offset: end_index + 2]) if bottom_line else False

            if adj_left or adj_right or adj_top or adj_bot:
                sum_nums += number

        end_index += 1

    return sum_nums


with open("day3.txt", "r") as txt_file:
    sum_part_nums: int = 0

    list_lines: list[str] = txt_file.readlines()  # reads (loads into memory) all the lines into a list at once, separating them at each "\n"
    list_lines = list(map(str.rstrip, list_lines))  # removes trailing newline character from each line
    max_chars = len(list_lines[0])  # 140 in this case

    first_line = list_lines[0]
    sum_part_nums += sum_adj_nums(first_line, None, list_lines[1])

    for i in range(1, len(list_lines) - 1):
        top_line = list_lines[i-1]
        line = list_lines[i]
        bottom_line = list_lines[i+1]

        sum_part_nums += sum_adj_nums(line, top_line, bottom_line)

    last_line = list_lines[-1]
    sum_part_nums += sum_adj_nums(last_line, list_lines[-2], None)


    print(sum_part_nums)


"""
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""


def scan_line(line: str, star_index: int) -> list[int]:
    nums_found: list[int] = []
    end_index = 0

    while end_index < max_chars:

        if line[end_index].isdigit():
            start_index = end_index

            while end_index + 1 < max_chars and line[end_index + 1].isdigit():
                end_index += 1

            number = int(line[start_index: end_index + 1])

            if any(abs(digit_index - star_index) <= 1 for digit_index in range(start_index, end_index + 1)):
                nums_found.append(number)

        end_index += 1

    return nums_found


with open("day3.txt", "r") as txt_file:
    sum_gear_ratios: int = 0

    top_line = txt_file.readline().rstrip()  # ".readline()" behaves line a generator that iterates via ".next()" method
    line = txt_file.readline().rstrip()
    bottom_line = txt_file.readline().rstrip()

    max_chars = len(line)

    while bottom_line:

        for j in range(max_chars):
            if line[j] == "*":
                adjacent_nums = scan_line(top_line, j) + scan_line(line, j) + scan_line(bottom_line, j)
                if len(adjacent_nums) == 2:
                    sum_gear_ratios += (adjacent_nums[0] * adjacent_nums[1])

        top_line = line
        line = bottom_line
        bottom_line = txt_file.readline().rstrip()

    print(sum_gear_ratios)
