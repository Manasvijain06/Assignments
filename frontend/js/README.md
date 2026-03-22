# Student Performance Analyzer

## 📌 Overview
This project is a simple console-based JavaScript program that I built to understand how to work with real-world data using arrays and objects.
The program analyzes student performance and calculates different results like total marks, average, subject-wise analysis, class topper, and grades.

---

## ⚙️ Technologies Used
- JavaScript (Basics)
- VS Code
- Node.js / Browser Console

---

## 📂 Project Structure
```
frontend/
├── js/
│   └── manasvi_student_analyzer.js
├── images/
│   ├── Average_marks.png
│   ├── Grade_logic.png
│   ├── Student_Data.png
│   ├── SubWise_AvgScore.png
│   ├── SubWise_HighestScore.png
│   ├── Total_Marks.png
│   └── class_Topper.png
└── README.md
```

---

## 📸 Output Screenshots

### 1. Student Data
![image_alt](https://github.com/Manasvijain06/Assignments/blob/27b1aee1e6aff9e49949d3286825359323aba5e0/frontend/js/Screenshots/Student_Data.png)

Adding the student data including Name, Subject, Marks(per subject) and attendance

---

### 2. Total Marks
![Total](https://github.com/Manasvijain06/Assignments/blob/27b1aee1e6aff9e49949d3286825359323aba5e0/frontend/js/Screenshots/Total_Marks.png)

Total marks are calculated by looping through each subject's scores and adding them together using a for loop inside a function.

---

### 3. Average Marks
![Average](https://github.com/Manasvijain06/Assignments/blob/27b1aee1e6aff9e49949d3286825359323aba5e0/frontend/js/Screenshots/Average_marks.png)

Here, the average marks are calculated by dividing total marks by number of subjects.

---

### 4. Subject-wise Highest
![Highest](https://github.com/Manasvijain06/Assignments/blob/27b1aee1e6aff9e49949d3286825359323aba5e0/frontend/js/Screenshots/SubWise_HighestScore.png)

The highest score for each subject is found by looping through all students and comparing their marks. The highest score and student name are updated whenever a higher value is found.

---

### 5. Subject-wise Average
![Subject Avg](https://github.com/Manasvijain06/Assignments/blob/27b1aee1e6aff9e49949d3286825359323aba5e0/frontend/js/Screenshots/SubWise_AvgScore.png)
This output displays the average score of each subject across all students.
It is done by dividing the totalScore by count.

---

### 6. Class Topper
![Topper](https://github.com/Manasvijain06/Assignments/blob/27b1aee1e6aff9e49949d3286825359323aba5e0/frontend/js/Screenshots/class_Topper.png)
This shows the student who got the highest total marks in the class.
It is done by using if comdition and comparing values.

---

### 6. Grade Output
![Grade](https://github.com/Manasvijain06/Assignments/blob/27b1aee1e6aff9e49949d3286825359323aba5e0/frontend/js/Screenshots/Grade_Logic.png)

Grades are assigned based on average marks:
- A → 85 and above  
- B → 70 to 84  
- C → 50 to 69  
- Fail → below 50  

A student is also marked as fail if:
- Any subject score is 40 or below  
- Attendance is less than 75%  

---

## Concepts Used
In this project, I practiced:
- Arrays and objects
- forEach loops
- Functions
- Conditional statements
- Nested loops

---

## 🎯 Learning Outcome
By doing this assignment, I learned how to:
- Work with structured data in JavaScript  
- Apply logic step by step  
- Solve real-world problems using loops and conditions  
- Write clean and understandable code  

---

## ▶️ How to Run
Run the file using Node.js:

node manasvi_student_analyzer.js
