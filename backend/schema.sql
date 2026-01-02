<!-- Create DATABASE module14demo;     
<!-- INSERT INTO movie (title, director, rating) VALUES ('Interstellar', 'Christopher Nolan', 10); -->



<!-- SCHEMA.SQL -->
CREATE TABLE IF NOT EXISTS movie (
    movie_id SERIAL, 
    title VARCHAR(200) NOT NULL,
    director VARCHAR(200) NOT NULL,
    rating INT NOT NULL,
    PRIMARY KEY (movie_id)
);

