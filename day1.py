# بسم الله الرحمن الرحيم وبه نستعين

"""
On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet7

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""
from rich import print


with open("day1.txt", "r") as text_file:
    values_total: int = 0
    line: str

    for line in text_file:  # reads the lines of the file lazily; one line at a time (memory-efficient because only one line is loaded into memory). Using the ".readlines()" method loads the entire file into memory (reads all lines at once)
        line = line.rstrip()  # remove the trailing newline character and whitespace
        first_dig = second_dig = None

        # Iterate from both ends towards the center:
        for i in range(len(line)):
            if first_dig is None and line[i].isdigit():
                first_dig = line[i]

            if second_dig is None and line[-1-i].isdigit():
                second_dig = line[-1-i]

            # Break out of the loop once both digits are found:
            if first_dig and second_dig:
                break

        values_total += int(first_dig + second_dig)

    print(values_total)


"""
Your calculation isn't quite right.s It looks like some of the digits are actually spelled out with letter: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""

digits_dict = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

with open("day1.txt", "r") as text_file:
    values_total: int = 0
    line: str

    for line in text_file:
        line = line.rstrip()
        first_dig = second_dig = None

        # Iterate from both ends towards the center:
        for i in range(len(line)):

            if first_dig is None:
                if line[i].isdigit():
                    first_dig = line[i]

                else:
                    for digit in digits_dict:
                        if digit in line[i:i+len(digit)]:
                            first_dig = digits_dict[digit]
                            break

            if second_dig is None:
                if line[-1-i].isdigit():
                    second_dig = line[-1-i]

                else:
                    for digit in digits_dict:
                        if digit in line[-len(digit)-i:]:
                            second_dig = digits_dict[digit]
                            break

            # Break out of the loop once both digits are found:
            if first_dig and second_dig:
                break

        values_total += int(first_dig + second_dig)

    print(values_total)
