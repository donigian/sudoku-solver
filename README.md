# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

###  How do we use constraint propagation to solve the naked twins problem? 
**Constraint Propagation** is all about using local constraints in a space to dramatically reduce the search space. In the case of Naked Twins, the constraint is that if the same box value pair appears in the  column unit or row unit, then all other boxes in the square unit cannot contain the pair of values in those two boxes. As we enforce each constraint, we see that it introduces new constraints for other parts of the board that can help us further reduce the number of possibilities. 

### How do we use constraint propagation to solve the diagonal sudoku problem?  
**Constraint Propagation** is all about using local constraints in a space to dramatically reduce the search space. In the case of Diagonal Sudoku, among the two main diagonals, the numbers 1 to 9 should all appear exactly once. As we enforce each constraint, we see that all other boxes on the diagonal cannot contain any values previously seen.

### Install

This project requires **Python 3**. You'll also want to download [Anaconda](https://www.continuum.io/downloads) in order to reproduce the results.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. Please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - Sudoku solver.
* `solution_test.py` - You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - This is code for visualizing Sudoku solver.
* `visualize.py` - This is code for visualizing Sudoku solver.

Here is a screenshot of a solved puzzle:
![Solved Puzzle](images/solved.png)

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in function.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.