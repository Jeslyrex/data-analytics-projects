-- ================================================
-- Student Academic Performance SQL Analysis
-- Author: Vanganuru John Jasmith
-- Tools: MySQL
-- Description: Relational database design + 15+
--              SQL queries for academic analytics
-- ================================================

-- ================================================
-- STEP 1: CREATE DATABASE & TABLES
-- ================================================

CREATE DATABASE IF NOT EXISTS student_academics;
USE student_academics;

CREATE TABLE IF NOT EXISTS Departments (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    established_year INT
);

CREATE TABLE IF NOT EXISTS Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),
    dept_id INT,
    admission_year INT,
    email VARCHAR(100),
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

CREATE TABLE IF NOT EXISTS Courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    dept_id INT,
    credits INT,
    semester INT,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

CREATE TABLE IF NOT EXISTS Grades (
    grade_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    semester INT,
    marks_obtained INT,
    max_marks INT,
    grade VARCHAR(5),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- ================================================
-- STEP 2: INSERT SAMPLE DATA
-- ================================================

INSERT INTO Departments (dept_name, hod_name, established_year) VALUES
('Computer Science', 'Dr. Ramesh Kumar', 2000),
('Electronics & Communication', 'Dr. Priya Sharma', 2001),
('Mechanical Engineering', 'Dr. Suresh Reddy', 1999),
('Civil Engineering', 'Dr. Lakshmi Devi', 2002),
('Information Technology', 'Dr. Anand Rao', 2003);

INSERT INTO Students (student_name, age, gender, dept_id, admission_year, email) VALUES
('Ravi Kumar', 20, 'Male', 1, 2022, 'ravi@college.com'),
('Priya Singh', 21, 'Female', 2, 2022, 'priya@college.com'),
('Arun Reddy', 20, 'Male', 1, 2022, 'arun@college.com'),
('Sneha Patel', 22, 'Female', 3, 2021, 'sneha@college.com'),
('Vikram Rao', 21, 'Male', 2, 2022, 'vikram@college.com'),
('Divya Nair', 20, 'Female', 1, 2022, 'divya@college.com'),
('Karan Shah', 22, 'Male', 4, 2021, 'karan@college.com'),
('Anjali Gupta', 21, 'Female', 5, 2022, 'anjali@college.com'),
('Rohit Verma', 20, 'Male', 1, 2022, 'rohit@college.com'),
('Meena Kumari', 21, 'Female', 2, 2022, 'meena@college.com'),
('Suresh Babu', 22, 'Male', 3, 2021, 'suresh@college.com'),
('Kavitha Rao', 20, 'Female', 5, 2022, 'kavitha@college.com'),
('Aditya Kumar', 21, 'Male', 4, 2022, 'aditya@college.com'),
('Pooja Sharma', 20, 'Female', 1, 2022, 'pooja@college.com'),
('Nikhil Reddy', 22, 'Male', 2, 2021, 'nikhil@college.com');

INSERT INTO Courses (course_name, dept_id, credits, semester) VALUES
('Data Structures', 1, 4, 3),
('Database Management Systems', 1, 4, 4),
('Python Programming', 1, 3, 2),
('Digital Signal Processing', 2, 4, 5),
('Circuit Analysis', 2, 3, 3),
('Thermodynamics', 3, 4, 3),
('Fluid Mechanics', 3, 4, 4),
('Structural Analysis', 4, 4, 4),
('Web Technologies', 5, 3, 3),
('Machine Learning', 1, 4, 6);

INSERT INTO Grades (student_id, course_id, semester, marks_obtained, max_marks, grade) VALUES
(1, 1, 3, 85, 100, 'A'),(1, 2, 4, 78, 100, 'B+'),
(1, 3, 2, 92, 100, 'A+'),(2, 4, 5, 76, 100, 'B+'),
(2, 5, 3, 88, 100, 'A'),(3, 1, 3, 65, 100, 'B'),
(3, 2, 4, 70, 100, 'B'),(3, 3, 2, 55, 100, 'C'),
(4, 6, 3, 82, 100, 'A'),(4, 7, 4, 74, 100, 'B+'),
(5, 4, 5, 90, 100, 'A+'),(5, 5, 3, 85, 100, 'A'),
(6, 1, 3, 95, 100, 'A+'),(6, 2, 4, 88, 100, 'A'),
(6, 10, 6, 91, 100, 'A+'),(7, 8, 4, 72, 100, 'B+'),
(8, 9, 3, 80, 100, 'A'),(9, 1, 3, 60, 100, 'B'),
(9, 3, 2, 58, 100, 'C'),(10, 4, 5, 83, 100, 'A'),
(10, 5, 3, 79, 100, 'B+'),(11, 6, 3, 68, 100, 'B'),
(12, 9, 3, 87, 100, 'A'),(13, 8, 4, 75, 100, 'B+'),
(14, 1, 3, 93, 100, 'A+'),(14, 2, 4, 86, 100, 'A'),
(15, 4, 5, 77, 100, 'B+'),(15, 5, 3, 82, 100, 'A');

-- ================================================
-- STEP 3: ANALYTICAL SQL QUERIES
-- ================================================

-- Query 1: Total students per department
SELECT d.dept_name, COUNT(s.student_id) AS total_students
FROM Departments d
LEFT JOIN Students s ON d.dept_id = s.dept_id
GROUP BY d.dept_name
ORDER BY total_students DESC;

-- Query 2: Top 5 students by average marks
SELECT s.student_name, d.dept_name,
       ROUND(AVG(g.marks_obtained), 2) AS avg_marks
FROM Students s
JOIN Grades g ON s.student_id = g.student_id
JOIN Departments d ON s.dept_id = d.dept_id
GROUP BY s.student_id, s.student_name, d.dept_name
ORDER BY avg_marks DESC
LIMIT 5;

-- Query 3: Pass/Fail analysis (pass = marks >= 50)
SELECT
    SUM(CASE WHEN marks_obtained >= 50 THEN 1 ELSE 0 END) AS passed,
    SUM(CASE WHEN marks_obtained < 50 THEN 1 ELSE 0 END) AS failed,
    ROUND(SUM(CASE WHEN marks_obtained >= 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pass_percentage
FROM Grades;

-- Query 4: Average marks per department
SELECT d.dept_name,
       ROUND(AVG(g.marks_obtained), 2) AS avg_marks,
       MAX(g.marks_obtained) AS highest_marks,
       MIN(g.marks_obtained) AS lowest_marks
FROM Departments d
JOIN Students s ON d.dept_id = s.dept_id
JOIN Grades g ON s.student_id = g.student_id
GROUP BY d.dept_name
ORDER BY avg_marks DESC;

-- Query 5: Grade distribution
SELECT grade, COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Grades), 1) AS percentage
FROM Grades
GROUP BY grade
ORDER BY count DESC;

-- Query 6: Students who scored above 85 in any subject
SELECT DISTINCT s.student_name, d.dept_name,
       c.course_name, g.marks_obtained
FROM Students s
JOIN Grades g ON s.student_id = g.student_id
JOIN Courses c ON g.course_id = c.course_id
JOIN Departments d ON s.dept_id = d.dept_id
WHERE g.marks_obtained > 85
ORDER BY g.marks_obtained DESC;

-- Query 7: Course wise average performance
SELECT c.course_name, c.credits,
       ROUND(AVG(g.marks_obtained), 2) AS avg_marks,
       COUNT(g.student_id) AS students_enrolled
FROM Courses c
JOIN Grades g ON c.course_id = g.course_id
GROUP BY c.course_id, c.course_name, c.credits
ORDER BY avg_marks DESC;

-- Query 8: Semester wise performance trend
SELECT semester,
       ROUND(AVG(marks_obtained), 2) AS avg_marks,
       COUNT(DISTINCT student_id) AS students_appeared
FROM Grades
GROUP BY semester
ORDER BY semester;

-- Query 9: Gender wise average performance
SELECT s.gender,
       ROUND(AVG(g.marks_obtained), 2) AS avg_marks,
       COUNT(DISTINCT s.student_id) AS total_students
FROM Students s
JOIN Grades g ON s.student_id = g.student_id
GROUP BY s.gender;

-- Query 10: Students with below average performance
SELECT s.student_name, d.dept_name,
       ROUND(AVG(g.marks_obtained), 2) AS avg_marks
FROM Students s
JOIN Grades g ON s.student_id = g.student_id
JOIN Departments d ON s.dept_id = d.dept_id
GROUP BY s.student_id, s.student_name, d.dept_name
HAVING avg_marks < (SELECT AVG(marks_obtained) FROM Grades)
ORDER BY avg_marks ASC;

-- Query 11: Top performing department
SELECT d.dept_name,
       ROUND(AVG(g.marks_obtained), 2) AS avg_marks
FROM Departments d
JOIN Students s ON d.dept_id = s.dept_id
JOIN Grades g ON s.student_id = g.student_id
GROUP BY d.dept_name
ORDER BY avg_marks DESC
LIMIT 1;

-- Query 12: Students with consistent A grades
SELECT s.student_name, COUNT(*) AS a_grades
FROM Students s
JOIN Grades g ON s.student_id = g.student_id
WHERE g.grade IN ('A', 'A+')
GROUP BY s.student_id, s.student_name
HAVING a_grades >= 2
ORDER BY a_grades DESC;

-- Query 13: Course difficulty ranking (lowest avg = hardest)
SELECT c.course_name,
       ROUND(AVG(g.marks_obtained), 2) AS avg_marks,
       CASE
           WHEN AVG(g.marks_obtained) >= 80 THEN 'Easy'
           WHEN AVG(g.marks_obtained) >= 65 THEN 'Medium'
           ELSE 'Hard'
       END AS difficulty
FROM Courses c
JOIN Grades g ON c.course_id = g.course_id
GROUP BY c.course_id, c.course_name
ORDER BY avg_marks ASC;

-- Query 14: Department KPI summary report
SELECT d.dept_name,
       COUNT(DISTINCT s.student_id) AS total_students,
       COUNT(g.grade_id) AS total_exams,
       ROUND(AVG(g.marks_obtained), 2) AS avg_marks,
       SUM(CASE WHEN g.marks_obtained >= 50 THEN 1 ELSE 0 END) AS passed,
       SUM(CASE WHEN g.marks_obtained < 50 THEN 1 ELSE 0 END) AS failed
FROM Departments d
LEFT JOIN Students s ON d.dept_id = s.dept_id
LEFT JOIN Grades g ON s.student_id = g.student_id
GROUP BY d.dept_name
ORDER BY avg_marks DESC;

-- Query 15: Student full report card
SELECT s.student_name, d.dept_name,
       c.course_name, c.semester,
       g.marks_obtained, g.max_marks, g.grade,
       ROUND(g.marks_obtained * 100.0 / g.max_marks, 1) AS percentage
FROM Students s
JOIN Grades g ON s.student_id = g.student_id
JOIN Courses c ON g.course_id = c.course_id
JOIN Departments d ON s.dept_id = d.dept_id
ORDER BY s.student_name, c.semester;