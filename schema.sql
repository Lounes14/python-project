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