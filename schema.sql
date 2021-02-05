CREATE TABLE angels (
    id BIGINT PRIMARY KEY,
    handle VARCHAR(50),
    name VARCHAR(50)
);

CREATE TABLE potential_founders ( 
    id BIGINT PRIMARY KEY,
    handle VARCHAR(50),
    name VARCHAR(50),
    description VARCHAR(300)
);

CREATE TABLE tweet (
    id BIGINT PRIMARY KEY,
    tweet TEXT, 
    created_at DATE,
    author_id BIGINT,
    liked_by_id BIGINT,
    FOREIGN KEY (author_id)
        REFERENCES potential_founders(id),
    FOREIGN KEY (liked_by_id)
        REFERENCES angels(id)
);