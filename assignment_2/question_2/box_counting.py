import numpy as np
import matplotlib.pyplot as plt

def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    assert h % nrows == 0, f"{h} rows is not evenly divisible by {nrows}"
    assert w % ncols == 0, f"{w} cols is not evenly divisible by {ncols}"
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))


def box_counting(grid):
    grid = np.asarray(grid)
    dims = [2, 4, 8, 16, 32]

    expected_sum = grid.sum()
    box_dict = {}
    for dim in dims[::-1]:
        boxes_used = 0
        current_sum = 0
        if dim < grid.shape[0]:
            boxes = blockshaped(grid, dim, dim)
            num_boxes = boxes.shape[0]

            for box in range(num_boxes):
                coverage = boxes[box].sum()

                if coverage > 0:
                    boxes_used += 1
                    current_sum += coverage

        box_dict[dim] = boxes_used

    return box_dict


world = np.genfromtxt("assignment_2/question_2/2021-10-24T20:26:45.969/grid.csv", delimiter=",")
num_boxes = box_counting(world)
print("Num boxes:", num_boxes)
x = []
y = []
for key in num_boxes.keys():
  x.append(key)
  y.append(num_boxes[key])

x = np.log10(np.asarray(x))
plt.scatter(x, np.log10(y))
m, b = np.polyfit(x, np.log10(y), 1)
plt.plot(x, m*x + b)
plt.title('Dimensionality: ' + str(-m))
plt.xlabel('Log 10 of Box Size')
plt.ylabel('Log 10 of Number of Boxes')
plt.savefig("assignment_2/question_2/2021-10-24T20:26:45.969/dimensionality.png")
