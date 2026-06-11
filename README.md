Sudoku Solver Web App Overview

image image image
Working link: https://sudoku-solver-sv3kefefpdu3tx9npvgmsn.streamlit.app/ This project is a Sudoku Solver Web Application that allows users to upload or input a Sudoku puzzle and get the solved grid instantly. It uses a backtracking algorithm (or image processing + solver, depending on your version) to compute the solution efficiently.

Features

Automatic Sudoku solving using backtracking algorithm
Image input support (if enabled in your version)
Manual grid input option
Fast and accurate solution generation
Simple and interactive web interface (Streamlit / Flask)
Tech Stack

Python
OpenCV (for image processing)
NumPy
Streamlit / Flask (for web UI)
Backtracking Algorithm (core solver logic)
Project Structure

sudoku-solver/ │── app.py # Main web app │── solver.py # Sudoku solving algorithm │── image_processor.py # Image to grid extraction (if used) │── utils.py # Helper functions │── requirements.txt # Dependencies │── README.md

How It Works

User uploads an image or enters a Sudoku grid
If image input is used, it is processed to extract digits
The solver applies a backtracking algorithm to fill empty cells
The solved Sudoku grid is displayed on the UI
Algorithm The solver uses backtracking, which:

Tries filling empty cells with valid numbers (1–9)
Checks row, column, and 3×3 box constraints
Backtracks when a conflict occurs
Repeats until the puzzle is solved
