from ..db import db


def insert_ds_userid(member):
    tmp_none = "None"
    db.execute("INSERT OR IGNORE INTO user_info (UserID, User_Tel_Tag, User_Role) VALUES (?, ?, ?)", member.id,
               tmp_none, tmp_none)
    print(f"{member.id} was added in the DB")


def insert_tg_tag(member, tag):
    db.execute(f"UPDATE user_info SET User_Tel_Tag = ? WHERE UserID = ?", tag, member.id)
    print(f"Telegram tag {tag} was added in the DB for the user {member.name} with id {member.id}")
