CREATE TABLE IF NOT EXISTS exp (
    UserID integer PRIMARY KEY,
    UserXP integer DEFAULT 0,
    UserLevel integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_info (
    UserID integer PRIMARY KEY,
    User_Tel_Tag text,
    User_Role text
);