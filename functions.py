#Функция, создающая структуру БД (таблицы)
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE phone;
            DROP TABLE clients;
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
            id_client SERIAL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            surname VARCHAR(20) NOT NULL,
            email VARCHAR(50));
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
            id_phone SERIAL PRIMARY KEY,
            phone CHAR(11),
            id_client INTEGER REFERENCES clients(id_client));
            """)
        conn.commit()

#Функция, позволяющая добавить нового клиента
def add_client(conn, id_client, name, surname, email):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO clients(id_client, name, surname, email) VALUES(%s,%s,%s,%s) RETURNING id_client, name, surname, email;
    """,(id_client, name, surname, email))
        print(cur.fetchall())
        conn.commit()

#Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, id_phone, phone, id_client):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone(id_phone, phone, id_client) VALUES(%s,%s,%s) RETURNING id_phone, phone, id_client;
            """,(id_phone, phone, id_client))
        print(cur.fetchall())
        conn.commit()


#Функция, позволяющая изменить данные о клиенте
def change_client(conn, id_client, name=None, surname=None, email=None, phones=None):
    with conn.cursor() as cur:
        arg_list = {'name': name, 'surname': surname, 'email': email}
        for key, arg in arg_list.items():
            if arg:
                cur.execute(f"""
                UPDATE clients SET {key}=%s WHERE id_client=%s;
                """, (arg, id_client)
                )
                conn.commit()
        if phones:
            for old_phone, new_phone in phones.items():
                cur.execute("""
                UPDATE phone SET phone=%s WHERE phone=%s AND id_client=%s;
                """, (new_phone, old_phone, id_client)
                )
                conn.commit()

        cur.execute("""
        SELECT * FROM clients;
        """)
        print(cur.fetchall())

        cur.execute("""
        SELECT * FROM phone;
        """)
        print(cur.fetchall())
        
        


#Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(conn, id_client, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone WHERE id_client=%s AND phone=%s;
            """, (id_client, phone)
                )
        conn.commit()
        cur.execute("""
        SELECT * FROM phone;
        """)
        print(cur.fetchall())



#Функция, позволяющая удалить существующего клиента
def delete_client(conn, id_client):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone WHERE id_client=%s;
            """, (id_client,)
                )
        cur.execute("""
            DELETE FROM clients WHERE id_client=%s;
            """, (id_client,)
                )
        cur.execute("""
        SELECT * FROM clients;
        """)
        print(cur.fetchall())
    conn.commit()

            
#Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
def find_client(conn, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        arg_list = {'name': name, 'surname': surname, 'email': email}
        for key, arg in arg_list.items():
            if arg:
                cur.execute(f"""
                SELECT * FROM clients WHERE {key}=%s; 
                """, (arg,)
                )
                print(cur.fetchall())
        if phone:
            cur.execute("""
                    SELECT id_client FROM phone WHERE phone=%s; 
                    """, (phone,)
                    )
            id_client = cur.fetchone()

            cur.execute(
            """
            SELECT * FROM clients WHERE id_client=%s; 
            """, (id_client,)
            )
            print(cur.fetchall())

