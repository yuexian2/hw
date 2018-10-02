"""
590PR Fall 2018
Assignment 4, on Numpy

I provided you both a small and two very large 3-D ndarrays of signed numbers.
Their dimensions are such that they are cubes.

For the small array, you can see the complete expected output results in the
Doctest below.

You are to complete the function that will search all sub-cubes of the
full ndarray, to find the sub-cube whose 'surface' has the largest sum.
Borrowing terminology from set theory, where a set is still an 'improper'
subset of itself, the full cube has to be checked as a possibility as
well as all possible smaller subcubes within it.

Additionally, it should be able to print the intermediate results for
each size of subcube, as shown in the example test output with size 5.
"""

import numpy as np


def find_max_subcube(a: np.ndarray, show_intermediate_results=True) -> np.ndarray:
    """Given a cubical ndarray, search all subcubes (all proper and the improper one
    which is the whole thing), to find which one has the maximum sum of all cells
    in its outer layer. Since there are negative numbers in the values, there's no
    way to predict where it will be, and there's no theoretical advantage for
    largest subcubes vs medium ones.

    Note, to make the tests work on different OS platforms & hardware, all computed
    outputs are formatted to 2 decimal places. Also note that using the round() function
    on floats sometimes will not always produce the desired number of digits.
    So use string.format() instead, like shown in the test below.

    :param a: the whole array to search
    :param show_intermediate_results: whether to print results per subcube size
    :return: the subcube ndarray that had max sum

    >>> cube_size_5 = np.load(file='A4_cube_size_5.npy', allow_pickle=False, mmap_mode=None)
    >>> print('{:0.2f}'.format(cube_size_5[4,4,4]))
    -97.09
    >>> m = find_max_subcube(cube_size_5)  #doctest: +NORMALIZE_WHITESPACE
    searching cube of width 5
    checking all subcubes of width  1, of which     125 exist.  Highest sum    95.15 found at position (3, 4, 2)
    checking all subcubes of width  2, of which      64 exist.  Highest sum   355.41 found at position (1, 3, 3)
    checking all subcubes of width  3, of which      27 exist.  Highest sum   384.71 found at position (0, 0, 1)
    checking all subcubes of width  4, of which       8 exist.  Highest sum   503.98 found at position (0, 1, 1)
    checking all subcubes of width  5, of which       1 exist.  Highest sum   297.94 found at position (0, 0, 0)
    <BLANKLINE>
    Total number of subcubes checked: 225
    Highest sum found was 503.98 in a subcube of width 4 at position (0, 1, 1)
    >>> cube_size_60 = np.load(file='A4_cube_size_60.npy', allow_pickle=False, mmap_mode=None)
    >>> m = find_max_subcube(cube_size_60, show_intermediate_results=False)  #doctest: +NORMALIZE_WHITESPACE
    Total number of subcubes checked: 3348900
    Highest sum found was 29831.55 in a subcube of width 52 at position (0, 2, 3)
    """
    import numpy as np
    width=range(1,a.shape[0]+1)
    # cube_size_5 = np.load(file='A4_cube_size_5.npy', allow_pickle=False, mmap_mode=None)
    length = len(a[0])
    NumberofWidth = []
    sum_i_max = []
    index_i = []
    for i in width:
        if i<=2:
            maximum =a[0:i,0:i,0:i].sum()
        else:
            maximum = a[0:i,0:i,0:i].sum()- a[1:i-1,1:i-1,1:i-1].sum()
        index = (0, 0, 0)
        k = 0
        count = 0
        # print(k)
        while k + i - 1 != int(length):
            j = 0
            h = 0
            count = count + 1
            # sum_of_cube = cube_size_5[k - 1:k - 1 + i, j:j+i, h:h+i].sum()
            for j in range(length - i + 1):
                # sum_of_cube = cube_size_5[k - 1:k - 1 + i, j:j + i, h:h + i].sum()
                # print(j)
                for h in range(length - i + 1):
                    sum_of_cube = a[k:k + i, j:j + i, h:h + i].sum()
                    if i > 2:
                        sum_of_cube = sum_of_cube - a[k + 1:k + i - 1, j + 1:j - 1 + i, h + 1:h + i - 1].sum()
                    if maximum < sum_of_cube:
                        maximum = sum_of_cube
                        index = (k, j,h)
                    # print(h)
            k = k + 1
        sum_i_max.append(maximum)
        index_i.append(index)
        number = count * count * count
        NumberofWidth.append(number)
    highest_sum = max(sum_i_max)
    width_of_highest_cube = sum_i_max.index(highest_sum)+1
    origin_of_cube = index_i[sum_i_max.index(highest_sum)]
    target_array=a[origin_of_cube[0]:origin_of_cube[0]+width_of_highest_cube,origin_of_cube[1]:origin_of_cube[1]+width_of_highest_cube,origin_of_cube[2]:origin_of_cube[2]+width_of_highest_cube]
    print(target_array)
    print(highest_sum)
    print(width_of_highest_cube)
    print(origin_of_cube[1])
    # print(index_i)
    # print(sum_i_max)
    # print(NumberofWidth
    if length == 5:
        file_name ='output_cube5_yuexian'
    if length == 60:
        file_name = 'output_cube60_yuexian'
    if length == 100:
        file_name = 'output_cube100_yuexian'
    f = open(file_name, 'w')
    if show_intermediate_results:
        print('searching cube of width {}\n'.format(length),file=f)
        for num in range(len(index_i)):
            print("checking all subcubes of width {}\t, of which{:>8d} exist.  Highest sum {:>8.2f}  found at position {}".format(width[num], NumberofWidth[num], sum_i_max[num],index_i[num]), file=f)
    print('Total number of subcubes checked: {}'.format(sum(NumberofWidth)),file=f)
    print('Highest sum found was {:.2f}\t in a subcube of width {}\t at position {}\t'.format(max(sum_i_max),width[sum_i_max.index(max(sum_i_max))],index_i[sum_i_max.index(max(sum_i_max))]), file=f)
    return target_array
if __name__ == '__main__':
    #cube = np.load(file='A4_cube_size_60.npy', allow_pickle=False, mmap_mode=None)
    cube = np.load(file='A4_cube_size_100.npy', allow_pickle=False, mmap_mode=None)
    #

    cube = np.load(file='A4_cube_size_5.npy', allow_pickle=False, mmap_mode=None)
    sc = find_max_subcube(cube)


