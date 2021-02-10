COPY (
    /*
    SELECT angel.name, founder.name, founder.handle, founder.description
    FROM tweets
    INNER JOIN angels AS angel ON tweets.liked_by_id = angel.id
    INNER JOIN potential_founders AS founder ON tweets.author_id = founder.id
    */ 
    SELECT DISTINCT founder.name, founder.handle, founder.description
    FROM tweets
    INNER JOIN potential_founders as founder ON tweets.author_id = founder.id

) TO '/Users/drew/Documents/dev/twitter/test.csv' DELIMITER ',' CSV HEADER;
