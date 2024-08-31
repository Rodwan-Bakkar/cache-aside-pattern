CREATE DATABASE IF NOT EXISTS grocerydb;
USE grocerydb;

CREATE TABLE fruit (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    quantity INT
);

INSERT INTO fruit (id, name, quantity) VALUES (1, 'apple', 100);
INSERT INTO fruit (id, name, quantity) VALUES (2, 'orange', 200);
INSERT INTO fruit (id, name, quantity) VALUES (3, 'pear', 300);
