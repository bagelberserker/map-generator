# map-generator

I was inspired after seeing a heatmap of a random walk in 2 dimensions on wikipedia.


Increments values of an MxN matrix, determined by a psuedo-random walk.
Final values can be / are then treated as topographical heights.

[ENGLISH:]
It makes a grid, and every space has the number 0.
Then it puts a "walker" in the middle.
The walker then travels around the grid one space at a time, picking its direction at random.
Each time the walker steps on a space, it increases the number on that space by +1.
After the walker is done walking, the program creates and colors a map based on the numbers on the grid.
It treats those numbers as if they were measuring height above sea level:
  0 = blue, for the ocean
  1+ = green, for land
  The heigher the number, the lighter the shade of green, to represent mountains.
There are also other "filters" in the code that allow you to do a few different things, such as:
  Change what the walker does when it hits a wall
  Remove "strings" connecting islands together
  Fill in large lakes

In my opinion, the best results come from emulating islands.


Further explanations/elaborations can be found within the code's comments.
