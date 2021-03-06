# Experimental Comparison of Network Layout Algorithms: Majorization vs Stochastic Gradient Descent
![Figure7](systematic.png)
Code for producing Figure 7 in the paper [Graph Drawing by Stochastic Gradient Descent](https://arxiv.org/abs/1710.04626). The code produces the errorbar plots, and Inkscape was used to add the various .png layouts included in the repo. Code used to produce the data can be found in the separate repo <https://github.com/jxz12/s_gd2>.

## Abstract
Networks are often visualised by embedding them into two dimensions. A common method of finding such an embedding is by numerically optimising a function known as 'stress'. This figure shows an experimental study comparing the old state-of-the-art algorithm for optimising stress, known as majorization, and a new and more efficient algorithm known as stochastic gradient descent (SGD). We ran both algorithms 25 times upon 243 networks taken from the SparseSuite Matrix Collection (<https://sparse.tamu.edu/>). Each network maps to a single error bar along the x-axis, and the y-axis measures minimum and maximum values of stress over all runs, normalised to the best stress found on any run. The top half of the plot shows runs when both algorithms are limited to a fixed amount of runtime, and the bottom shows when allowed to run until the result can no longer be improved.

A video of the top plot shown for all timesteps in sequence can be viewed at https://youtu.be/uv6Vw36KZ0k, which further shows the behaviour of both algorithms using the time dimension.
