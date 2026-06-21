# Python Practice Assignments

This repository contains Python programs covering core to advanced concepts.

---

# Structure

```
python_advance/
├── exception_handling/
├── iterators_generators/
├── functional_programming/
├── regular_expressions/
├── testing_and_debugging/
├── packaging/
└── parallel_execution/
```

---

## 1. Exception Handling

```
|QNo.| Description                                     |
|----|-------------------------------------------------|
| q1 | Handle invalid integer input using ValueError   |
| q2 | Handle division by zero using ZeroDivisionError |
| q3 | Read number from file and handle exceptions     |
| q4 | Handle multiple exceptions in one program       |
| q5 | Catch all exceptions and display error message  |
| q6 | Raise error for negative numbers                |
| q7 | Create custom exception for age validation      |
| q8 | Handle file not found error                     |
```

---

## 2. Iterators and Generators

```
|QNo.| Description                                      |
|----|--------------------------------------------------|
| q9 | Iterate list using iterator and next()           |
| q10| Create custom iterator from 1 to N               |
| q11| Generate square numbers using generator          |
| q12| Generate Fibonacci sequence                      |
| q13| Generate even numbers using generator expression |
| q14| Compare iterator vs generator                    |
| q15| Process large data using generator               |
| q16| Use built-in generator (range)                   |
```

---

## 3. Functional Programming

```
|QNo.| Description                            |
|----|----------------------------------------|
|q17 | Square using lambda                    |
|q18 | Transform list using map()             |
|q19 | Filter even numbers using filter()     |
|q20 | Find product using reduce()            |
|q21 | Factorial using recursion              |
|q22 | Fibonacci using recursion              |
|q23 | Convert loop logic to functional style |
```

---

## 4. Regular Expressions

```
|QNo.| Description                     |
|----|---------------------------------|
|q24 | Extract numbers from string     |
|q25 | Validate email address          |
|q26 | Validate mobile number          |
|q27 | Search word using regex         |
|q28 | Find capitalized words          |
|q29 | Replace multiple spaces         |
|q30 | Check alphabets only            |
|q31 | Password validation using regex |
```

---

## 5. Testing and Debugging

```
|QNo.| Description                      |
|----|----------------------------------|
|q32 | Pytest for addition function     |
|q33 | Pytest for prime check           |
|q34 | Debug logical error using pdb    |
|q35 | Use breakpoints in loop          |
|q36 | IDE debugger vs print statements |
```

---

## 6. Packaging

```
|QNo.| Description                          |
|----|--------------------------------------|
|q37 | Create and import module             |
|q38 | Module vs package difference         |
|q39 | Create package with multiple modules |
|q40 | Math operations package              |
```

---

## 7. Parallel Execution – Threading & Multiprocessing

```
|QNo.| Description                            |
|----|----------------------------------------|
|q41 | Run multiple threads simultaneously    |
|q42 | Thread for sum calculation             |
|q43 | Use join() in threading                |
|q44 | Simulate file downloads using threads  |
|q45 | Create processes and print PID         |
|q46 | Multiprocessing for square calculation |
|q47 | ThreadPoolExecutor usage               |
|q48 | ProcessPoolExecutor usage              |
```

---

## How to Run

## Running Individual Programs

```bash
# Navigate to specific topic folder
cd exception_handling

# Run a program
python q1.py

# Run with input
echo "25" | python q1.py
```

---

# Running with pytest

```bash
# Install pytest (if not already installed)
pip install pytest

# Run all tests in testing_debugging folder
pytest testing_debugging/

# Run specific test file
pytest testing_debugging/q32.py -v

```

---

# Using the pdb Debugger

```bash
python -m pdb testing_debugging/q34.py
```

```
Inside pdb commands:
l → List code
n → Next line execution
s → Step into function
c → Continue execution
p variable → Print variable value
q → Quit debugger
```

---

Author - Manasvi Jain
