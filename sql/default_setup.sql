-- use realtime;
DROP TABLE users;
create table users
(
    id          VARCHAR(50) PRIMARY KEY,
    first_name  VARCHAR(50)  NOT NULL,
    middle_name VARCHAR(50),
    last_name   VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) NOT NULL,
    age         INT          NOT NULL,
    CONSTRAINT pk_alt CHECK ( first_name <> '' and last_name <> '' and email <> '')
);
