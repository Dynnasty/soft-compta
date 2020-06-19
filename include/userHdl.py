from sqlInit import init_db
from sqlFuncs import insert_table, print_table, delete_row

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

def delete_user(conn, username):
    rows = print_table(conn, "users")
    for row in rows:
        print(row[1])
        if (row[1] == username):
            user_id = row[0]

    delete_row(conn, "users", user_id)
    print("User " + username + " sucessfuly deleted")