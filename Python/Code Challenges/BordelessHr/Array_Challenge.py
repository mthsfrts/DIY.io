# This challenge was a part of an assessment series from BorderlessHR Company.

"""
Difficulty: Hard
Description: For this challenge you will determine how many times you can jump around within an array.

___________________________________________________________________________________________________________________
Challenge:

Have the function ArrayChallenge(arr) take the array of numbers stored in arr and first determine the largest
element in the array, and then determine whether you can reach that same element within the array by moving left or
right continuously according to whatever integer is in the current spot. If you can reach the same spot within the
array, then your program should output the least amount of jumps it took.

For example: if the input is [2, 3, 5, 6, 1] you'll start at the spot where 6 is and if you jump 6 spaces to the right
while looping around the array you end up at the last element where the 1 is.

Then from here you jump 1 space to the left, and you're back where you started, so your program should output 2.
If it's impossible to end up back at the largest element in the array your program should output -1.

The largest element in the array will never equal the number of elements in the array. The largest element will be
unique.

Input:1,2,3,4,2

Output:3

Input:1,7,1,1,1,1

Output:2
___________________________________________________________________________________________________________________
Assumptions

Assume largest element is unique
Largest element doesn't equal len(arr) > output > 1
Positive integers only
Number of Jumps is equal to the largest element


Code Output

The least amount of jumps to reach that same element within the array by moving left or
right continuously according to whatever integer is in the current spot
___________________________________________________________________________________________________________________
"""

# Here is my solution for this particular one.

array = [1, 2, 3, 4, 2]


def array_challenge(arr):
    """ This will return the least amount of jump need to reach the largest number spot of the array """

    output = {}  # New dictionary

    # Slicing the given array

    n = len(arr)  # Returns the length of the array.
    largest = max(arr)  # Returns the largest element of the array.
    index_position = arr.index(largest)  # Returns the position at the first occurrence of the specified value.

    print("Largest Element =", largest)
    print("Element Index Position =", index_position)

    for i in range(n):
        # This for will set and store the number jumps needed to reach the largest element
        # base on the length of the array.

        output[i] = (left(n, i, arr[i]), right(n, i, arr[i]))

    if index_position in output[index_position]:
        return 1

    jump_set = set(output[index_position])  # Will create an unordered collection of elements.

    for step in range(2, n):
        # This for will set the least number jumps needed to reach the largest element.
        for i in tuple(jump_set):
            jump_set.add(output[i][0])
            jump_set.add(output[i][1])

        if index_position in jump_set:
            return step
    return -1


def left(length, position, element):
    """
    This will return the number of jumps you need to do to de right position of the element
    to be able to loop back to the same spot.
    """
    left = element % length
    if left > position:
        left = length + position - left

    else:
        left = position - left

    return left


def right(length, position, element):
    """
    This will return the number of jumps you need to do to de right position of the element
    to be able to loop back to the same spot.
    """
    right = element % length
    if right > length - position - 1:
        right = right + position - length

    else:
        right = position + right

    return right


# keep this function call here
print(array_challenge(array))
