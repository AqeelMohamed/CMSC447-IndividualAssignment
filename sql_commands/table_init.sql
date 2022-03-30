-- table_init.sql
--      Initialize the SQLite table with the sample test data that was provided
--      !!! This should only be called on the FIRST TIME THE CODE IS RAN !!!
--      CTRL + Shift + Q     -> Run SQL Query -> Requires SQLite Extension on VSCode published by alexcvzz

-- To be safe, drop all entries in the three tables to make sure we don't reinsert anything important
DELETE FROM course;
DELETE FROM instructor;
DELETE from student;

-- Insert all sample courses into course table
INSERT INTO course (course_id, instructor_id, title)
VALUES 
    (8415, 654, 'Differential Equations'),
    (5641, 894, 'Organic Chemistry'),
    (8249, 874, 'Software Engineering'),
    (8929, 874, 'Machine Learning');

SELECT * FROM course;

-- Insert all sample instructors into instructor table
INSERT INTO instructor(instructor_id, name, department)
VALUES
    (654, 'Kim Hwang', 'Mathematics'),
    (894, 'Aaron Powell', 'Chemistry'),
    (843, 'Ryan Sampson', 'Physics'),
    (984, 'Dakota Robertson', 'Biology'),
    (874, 'Dale Sanders', 'Computer Science'),
    (795, 'Mason Flynn', 'Environmental Science'),
    (967, 'Blake Smith', 'Mathematics');

SELECT * FROM instructor;

-- Insert all sample students into student table
INSERT INTO student(student_id, credits_earned, name)
VALUES
    (211, 54, 'Cameron Suarez'),
    (122, 12, 'Uzoma Okoye'),
    (213, 17, 'Irma Schwartz'),
    (524, 100, 'Chandra Choudhary'),
    (425, 49, 'Shea McNamara'),
    (626, 62, 'Cameron Johnson'),
    (287, 87, 'Taylor Ellison');

SELECT * FROM student;