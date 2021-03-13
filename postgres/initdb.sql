CREATE TABLE warning(
    id varchar(19) NOT NULL,
    name varchar(32) NOT NULL,
    enforcer varchar(32) NOT NULL,
    reason  varchar(180) NOT NULL,
    server varchar(50),
    warned_on date DEFAULT CURRENT_DATE
)