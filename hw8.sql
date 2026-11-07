--SELECT * FROM assignment;
--SELECT * FROM submissions;
--SELECT * FROM users;


-- A) все сдачи студента по фамилии 
/* 
SELECT	users.id,
		users.full_name as 'Имя студента',
		assignment.pair_number AS 'Номер пары',
        assignment.title AS 'Тема пары',
        submissions.link AS 'Ссылка на дз',
        submissions.status AS 'Статус выполнения',
        submissions.created_at AS 'Время сдачи'
FROM submissions
JOIN users ON users.id = submissions.student_id
JOIN assignment on assignment.id = submissions.assignment_id 
*/


-- B) сколько сдач пришло на каждое задание (JOIN + COUNT + GROUP BY)
/*
--если надо посчитать количество студентов сдавших каждую работу:
--SELECT assignment.pair_number, assignment.title, COUNT(DISTINCT submissions.student_id) AS submissions_cnt
SELECT assignment.pair_number, assignment.title, COUNT(submissions.id) AS submissions_cnt
FROM assignment
FULL JOIN submissions ON submissions.assignment_id = assignment.id
GROUP BY assignment.id, assignment.pair_number, assignment.title
*/


-- C) студенты, не сдавшие ни одной работы (LEFT JOIN … IS NULL или NOT EXISTS, + роль)
/*
SELECT users.full_name, users.group_name, users.telegram, submissions.assignment_id
FROM users
LEFT JOIN submissions ON submissions.student_id = users.id
WHERE users.role = 'STUDENT' AND submissions.id IS NULL
*/