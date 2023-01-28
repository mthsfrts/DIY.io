"""
Difficulty: Hard

Maximum Score: 15

Description: For this challenge you will be transposing rows and columns within an array.

Have the function MatrixChallenge(strArr) read the strArr parameter being passed which will represent an NxN matrix filled with 1's and 0's.
Your program should determine the number of swaps between two rows or two columns that must be made to change the matrix such that the border of the matrix
contains all 1's and the inside contains 0's.
The format of strArr will be: ["(n,n,n...)","(...)",...] where n represents either a 1 or 0.
The smallest matrix will be a 3x3 and the largest will be a 6x6 matrix.

For example: if strArr is: ["(0,1,1)","(1,1,1)","(1,1,1)"] then you can swap the first two columns and then swap
the first two rows to create a matrix with the 1's on the border and the 0 on the inside, therefore your program
should output 2.

Examples
Input: ["(0,1,1)","(1,1,1)","(1,1,1)"]

Output: 2

Input: ["(0,1,0,1)","(1,1,1,1)","(0,1,0,1)","(1,1,1,1)"]
Output: 2

"""

srtArr = ["(0, 1, 1)",
          "(1, 1, 1)",
          "(1, 1, 1)"]

"""
srtArr = [(0, 1, 0, 1),
          (1, 1, 1, 1),
          (0, 1, 0, 1),
          (1, 1, 1, 1)]
"""

def MatrixChallenge(strArr):
    n = len(strArr)
    swap_count = 0

    # Creating the matrix
    for x in range(n):
        matrix = []
        for y in range(len(strArr[x])):
            if strArr[x][y] == "1" or strArr[x][y] == "0":
                matrix.append(strArr[x][y])

        # Analyzing the matrix to assure no border has a 0
        for row in range(len(matrix)):
            for col in range(int(matrix[row])):

                # condition to check the borders only
                if row == 0 or row == len(matrix) - 1 or col == 0 or col == len(matrix[row]) - 1:
                    if matrix[row][col] == "0":
                        # column needs to be swapped
                        if col == 0 or col == len(matrix[row]) - 1:
                            SwapColumn(matrix, col)
                            swap_count = swap_count + 1

                        # row needs to be swapped
                        elif row == 0 or row == len(matrix) - 1:
                            SwapRow(matrix, row)
                            swap_count = swap_count + 1

        print(matrix)

    print(swap_count)

    return swap_count


def SwapColumn(matrix, col):
    # Traverse to find a column that we can swap with
    for y in range(len(matrix[0])):

        # ignore same column or border columns
        if y == col or y == 0 or y == len(matrix[0]) - 1:
            continue

        else:
            valid = True

            # analyze current column to check if is valid for swapping
            for row in range(len(matrix)):
                if matrix[row][y] == "0":
                    valid = False
                    break

            # preform the swap between the 2 columns
            if valid:
                for x in range(len(matrix)):
                    temp = matrix[x][col]
                    matrix[x][col] = matrix[x][y]
                    matrix[x][y] = temp

                    return


def SwapRow(matrix, row):
    # traverse to find a row that we can swap with
    for x in range(len(matrix)):

        # ignore the same row, or any border rows
        if x == row or x == 0 or x == len(matrix) - 1:
            continue

        else:
            valid = True

            # analyze current row to check if is valid for swapping
            for col in range(len(matrix[0])):
                if matrix[x][col] == "0":
                    valid = False
                    break

            # preform the swap between the 2 rows
            if valid:
                for y in range(len(matrix)):
                    temp = matrix[row][y]
                    matrix[row][y] = matrix[x][y]
                    matrix[x][y] = temp

                return


if __name__ == "__main__":
    MatrixChallenge(srtArr)
