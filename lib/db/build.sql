CREATE TABLE IF NOT EXISTS exp (
    UserID integer PRIMARY KEY,
    UserXP integer DEFAULT 0,
    UserLevel integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);