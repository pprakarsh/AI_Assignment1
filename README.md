# 8-Puzzle Problem

Solved using Astar Algorithm with expansing of nodes using Breadth First Search

Using Breadth First Search for expansion of nodes is useful when the goal state is beleived to be at some large distance
from the Initital state.
Expansion using Breadth First Search optimizes both space and time by calling for heuristic function (if overhead of Heuristic function high)
for far lesser number of nodes. 
For visualisation one can consider that the graph takes large steps at a time.

Skeleton of the work is described here:
1. Implementing the usual A * for 8-Puzzle, with the Expand function taking a “depth” parameter –
the depth to which each expand call expands.
2. Implementing both the usual heuristics: tile mismatch count and manhattan distance.
3. In the main function, read the depth parameter as input, got the InitialState and FinalState, and called the A *
solver twice for each heuristic: once with the input depth parameter, and then again with the
parameter being 1 (which is the usual Expand).
Thus the total number of times that the puzzle solved by A * is 4.
4. Compared the results of all the four calls for at least 10 randomly generated initial states for
optimality. 
5. Compared the computational costs (number of nodes generated and the maximum length of the
fringe throughout) of all the four calls for the different initial states.

