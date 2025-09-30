# Keymaster - An Intelligent Cipher Solver

A Python tool designed to automatically identify and break over a dozen classical ciphers using statistical and heuristic methods.

### Key Features
- **Heuristic-Based Analysis**: Uses statistical tests (Index of Coincidence, Kasiski Examination) to intelligently determine the most likely cipher type before attempting to solve.
- **Broad Cipher Support**: Includes solvers for over 12 classical ciphers, including substitution, transposition, Vigenère, Beaufort, and Hill ciphers.
- **Advanced Search**: Employs heuristic search techniques like simulated annealing to solve substitution, two-square and four-square ciphers.

### Usage
To run the solver, after cloning the repo and extracting the files, place your ciphertext in `input.txt` and execute the main script:
```bash
python main.py
```

### Credits
- ChatGPT 3.5 for implementing a small number of the simpler solvers from a detailed description (hill, some transposition ciphers)