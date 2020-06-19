from sqlInit import init_db
from sqlFuncs import insert_table, print_table

def create_user(conn, username, password, userlevel):
    rows = print_table(conn, "users")
    for row in rows:
        print(row[1])
        if (row[1] == username):
            print("create_user: Username already exists")
            return (84)

    user_infos = [username, password, userlevel]
    insert_table(conn, "users", user_infos)
    print("create_user: User " + username + " successful created with userlevel " + str(userlevel))
    return(200)