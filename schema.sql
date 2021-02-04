CREATE TABLE angels (
    handle VARCHAR(50),
    name VARCHAR(50),
);

CREATE TABLE potential_founders ( 
    handle VARCHAR(50),
    name VARCHAR(50),
    description VARCHAR(300),
);

CREATE TABLE liked_tweet (
    id INT PRIMARY KEY,
    tweet TEXT, 
    create_at DATE,
    author ,
    liked_by ,
);