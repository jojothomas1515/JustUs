-- use realtime;

DROP DATABASE if EXISTS justus;
CREATE DATABASE justus;
CREATE USER justus WITH PASSWORD 'justus_pwd';
GRANT ALL ON DATABASE justus TO justus;
ALTER DATABASE justus OWNER TO justus;
\c justus;
SET ROLE justus;
create table users
(
    id            VARCHAR(50) PRIMARY KEY,
    first_name    VARCHAR(50)  NOT NULL,
    middle_name   VARCHAR(50),
    last_name     VARCHAR(50)  NOT NULL,
    email         VARCHAR(200) NOT NULL,
    date_of_birth DATE,
    password      VARCHAR(200) not null,
    is_active     BOOLEAN,
    CONSTRAINT pk_alt CHECK ( first_name <> '' and last_name <> '' and email <> '')
);

create table friends
(
    requester_id    VARCHAR(50) NOT NULL,
    requested_id    VARCHAR(50) NOT NULL,
    status          VARCHAR(20) CHECK ( status = 'pending' or status = 'accepted' or status = 'rejected'),
    date DATE        NOT NULL,
    PRIMARY KEY (requester_id, requested_id),
    constraint fk_requester FOREIGN KEY (requester_id) REFERENCES users (id) ON DELETE CASCADE ,
    constraint fk_requested FOREIGN KEY (requested_id) REFERENCES users (id) ON DELETE CASCADE
);

create table messages
(
    id          VARCHAR(50) PRIMARY KEY,
    sender_id   VARCHAR(50) NOT NULL,
    receiver_id VARCHAR(50) NOT NULL,
    message     TEXT,
    timestamp   TIMESTAMP   NOT NULL,
    CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES users (id),
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES users (id)
)