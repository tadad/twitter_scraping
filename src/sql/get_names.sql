/*COPY (*/
    /*
    SELECT angel.name, founder.name, founder.handle, founder.description
    FROM tweets
    INNER JOIN angels AS angel ON tweets.liked_by_id = angel.id
    INNER JOIN potential_founders AS founder ON tweets.author_id = founder.id
    */ 
    SELECT DISTINCT angel.name, angel.handle, founder.name, founder.handle, founder.description, tweets.created_at
    FROM tweets
    INNER JOIN potential_founders as founder ON tweets.author_id = founder.id
    INNER JOIN angels as angel ON tweets.liked_by_id = angel.id
    WHERE tweets.created_at >= NOW() - interval '7 day' 

/*) TO '/Users/drew/Documents/dev/twitter/test.csv' DELIMITER ',' CSV HEADER*/
;