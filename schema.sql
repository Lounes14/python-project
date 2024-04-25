CREATE TABLE users (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username VARCHAR(50) NOT NULL UNIQUE,
                              password VARCHAR(100) NOT NULL
);
CREATE TABLE questions (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           question_text VARCHAR(255) NOT NULL
);

CREATE TABLE answers (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         question_id INT,
                         answer_text VARCHAR(255) NOT NULL,
                         is_correct BOOLEAN,
                         FOREIGN KEY (question_id) REFERENCES questions(id)
);

INSERT INTO answers (question_id, answer_text, is_correct) VALUES (1, 'Paris', TRUE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (1, 'Rome', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (1, 'Tokyo', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (2, 'Alger', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (2, 'Tokyo', TRUE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (2, 'Chicago', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (3, 'Elon Musk', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (3, 'Bill Gates', TRUE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (3, 'Larry Page', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (4, 'Tik Tok', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (4, 'Facebook', TRUE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (4, 'X', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (5, 'Anglais', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (5, 'Espagnol', TRUE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (5, 'Allemand', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (6, 'RAM', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (6, 'CPU', TRUE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (6, 'ROM', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (7, 'PHP', FALSE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (7, 'JavaScripts', TRUE);
INSERT INTO answers (question_id, answer_text, is_correct) VALUES (7, 'Python', FALSE