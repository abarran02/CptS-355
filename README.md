# WSU CptS 355 for Spring 2023

This repository includes all Haskell and Python programming assignments during my Spring 2023 semester in Programming Language Design. The class covered recursion, data flow, and unit testing, with the ultimate project being a PostScript interpreter with static scoping. Overall, this class pushed me to rethink how I write code by glancing into the inner working of programming languages, so that in the future I may write more efficient code with a better understanding of how and why it works.

## Labs

Labs 1 and 2 were written in Haskell. Lab 1 was an introduction to the language for getting familiar with the syntax and recursion requirement. Lab 2 added higher order functions such as `map`, `foldl` abd `foldr`, as well as trees and tail recursion.

Lab 3 was written in Python, and solved many of the same tasks as the previous labs. It focused on dictionaries, iteration, and the `map` and `reduce` functions.

## Homework

### Haskell

Homework 1 and 2 were arranged similarly to the labs. These reinforced writing functions with guards, using the tree data type, and the aforementioned higher order functions. Homework 1 also required my own unit tests using the `HUnit` library, which are included in `HW1Tests.hs`. Having previously avoided writing recursive functions, Haskell forced me to face my fears and think differently to solve problems. Code that I have written since does not have such an aversion to recursion.

### Python

Homework 3 was again arranged similarly to the labs, but also included writing my own iterator class to explore a typically implicit Python feature. This served as a warm-up exercise, and introduced the `unittest` library by having us write one unit test for each problem.

Homework 4 and 5 represented the bulk of the coursework with writing an interpreter for the defunct PostScript language by Adobe. The language's architecture is structured around a operation stack and a dictionary stack for storing operations, variables, and functions. The interpreter skeleton code was provided by the instructor. 

In Homework 4 parts 1 and 2, we were tasked with coding a subset of functions and flow control, such as `add`, `ifelse`, and `for`. These proved difficult to debug with VSCode's limited debug functionality, as stepping through the PostScript code also meant stepping through lots of repetitive Python code and hidden stacks. Yet again, we added our own unit tests, and I focused on writing well-known functions from other languages, such as `abs` or `and`.

After learning about static and dynamic scoping in class, Homework 5 asked us to add static scoping to the interpreter. This was accomplished by keeping track of the scope where a function or variable was defined using Activation Records in the dictionary stack. The dynamic scoping functionality was left in, so that the scoping rule can be called by a flag or function argument. I adapted some of my unit tests from Homework 4 for static scoping.
