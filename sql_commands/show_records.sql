-- SQLite
select student.name, course.title, record.grade
from student
join record
on student.student_id = record.student_id
join course 
on course.course_id = record.course_id