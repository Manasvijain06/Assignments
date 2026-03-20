/* 2.1 Given Data Structure */
const students = [
  {
    name: "Lalit",
    marks: [
      { subject: "Math", score: 78 },
      { subject: "English", score: 82 },
      { subject: "Science", score: 74 },
      { subject: "History", score: 69 },
      { subject: "Computer", score: 88 }
    ],
    attendance: 82
  },
  {
    name: "Rahul",
    marks: [
      { subject: "Math", score: 90 },
      { subject: "English", score: 85 },
      { subject: "Science", score: 80 },
      { subject: "History", score: 76 },
      { subject: "Computer", score: 92 }
    ],
    attendance: 91
  }
];

// storing all student data in a array of objects
// Each student object contains the name, marks (array of subjects), and attendance.

/* 2.2 Function to calculate total marks*/
function calculateTotalMarks(student) {
    let totalMarks = 0;

    // Loop through each subject's marks and add to totalMarks
    for(let i = 0; i < student.marks.length; i++) {
        totalMarks += student.marks[i].score;
    }   
    return totalMarks;
}   
// print total marks
students.forEach(student => {
    const totalMarks = calculateTotalMarks(student);
    console.log(student.name + " has total marks: " + totalMarks);
});

// Function to calculate average marks
function calculateAverage(student) {
  const total = calculateTotalMarks(student);

  // divide total by number of subjects
  return total / student.marks.length;
}

// print average marks
students.forEach(student => {
  const avg = calculateAverage(student);
  console.log(student.name + " Average Marks: " + avg);
});