import psycopg2

# Функция, создающая структуру БД (таблицы)
def create_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client_info (
            id SERIAL PRIMARY KEY,
            client_name VARCHAR(60) NOT NULL,
            client_last_name VARCHAR(60) NOT NULL,
            client_email VARCHAR(60) UNIQUE
        );
        CREATE TABLE IF NOT EXISTS phone_number (
            id_phone_number SERIAL PRIMARY KEY,
            id_client INTEGER REFERENCES client_info(id),
            client_number_phone VARCHAR(20) UNIQUE
        );
        """)

# Функция, позволяющая добавить нового клиента
def add_client(cur, name, last_name, email, phone_number):
        cur.execute("""
            INSERT INTO client_info(client_name, client_last_name, client_email) VALUES(%s, %s, %s) RETURNING id;
            """, (name, last_name, email))
        conn.commit()
        cur.execute("""
            INSERT INTO phone_number(client_number_phone, id_client) VALUES(%s, %s)
            """, (phone_number, cur.fetchone()))
        conn.commit()

# Функция, позволяющая добавить телефон для существующего клиента
def add_phone_number(cur, phone_number, id_client):
        cur.execute("""
            INSERT INTO phone_number(client_number_phone, id_client) VALUES(%s, %s)
            """, (phone_number, id_client))
        conn.commit()

# Функция, позволяющая изменить данные о клиенте
def change(cur, id_client, name="", last_name="", email="", phone=""):
        if name:
            cur.execute("""
                UPDATE client_info SET client_name=%s WHERE id=%s;
                """, (name, id_client))
        if last_name:
            cur.execute("""
                UPDATE client_info SET client_last_name=%s WHERE id=%s;
                """, (last_name, id_client))
        if email:
            cur.execute("""
                UPDATE client_info SET client_email=%s WHERE id=%s;
                """, (email, id_client))
        if phone:
            cur.execute("""
                SELECT id_phone_number from phone_number WHERE id_client=%s;
                """, (id_client,))
            cur.execute("""
                UPDATE phone_number SET client_number_phone=%s WHERE id_phone_number=%s;
                """, (phone, cur.fetchone()))
        conn.commit()

# Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(cur, id_client):
        cur.execute("""
            SELECT client_number_phone, id_phone_number FROM phone_number WHERE id_client=%s;
            """, (id_client,))
        list_number = cur.fetchall()
        if len(list_number) != 0:
            print(f"Список номеров для удаления:")
            [print(f'{i+1} - тел.{el[0]}') for i, el in enumerate(list_number)]
            delete_number = input('Введите цифру номера, который хотите удалить:')
            id_phone_number = list_number[int(delete_number) - 1][1]
            cur.execute("""
                DELETE FROM phone_number WHERE id_client=%s AND id_phone_number=%s;
                """, (id_client, id_phone_number))
        else:
            print('Нет номеров для удаления')
        conn.commit()

# Функция, позволяющая удалить существующего клиента
def delete_client(cur, id_client):
        cur.execute("""
            DELETE FROM phone_number WHERE id_client=%s;
                """, (id_client,))
        cur.execute("""
            DELETE FROM client_info WHERE id=%s;
                """, (id_client,))
        conn.commit()

# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client(cur):
    print("Искать по: \n"
          "Имени - введите 1 \n"
          "Фамилии - введите 2 \n"
          "По почте - введите 3 \n"
          "Номеру телефона- введите 4 \n")
    search_param = input("Введите номер поиска по параметру: ")
    if search_param == '1':
        search_info = input("Введите имя: ")
        cur.execute("""
            SELECT client_name, client_last_name, client_email, client_number_phone FROM client_info c
            JOIN phone_number p ON c.id = p.id_client
            WHERE client_name = %s
            """, (search_info,))
        print(cur.fetchall())
    if search_param == '2':
        search_info = input("Введите фамилию: ")
        cur.execute("""
            SELECT client_name, client_last_name, client_email, client_number_phone FROM client_info c
            JOIN phone_number p ON c.id = p.id_client
            WHERE client_last_name = %s
            """, (search_info,))
        print(cur.fetchall())
    if search_param == '3':
        search_info = input("Введите почту: ")
        cur.execute("""
            SELECT client_name, client_last_name, client_email, client_number_phone FROM client_info c
            JOIN phone_number p ON c.id = p.id_client
            WHERE client_email = %s
            """, (search_info,))
        print(cur.fetchall())
    if search_param == '4':
        search_info = input("Введите номер телефона: ")
        cur.execute("""
            SELECT client_name, client_last_name, client_email, client_number_phone FROM client_info c
            JOIN phone_number p ON c.id = p.id_client
            WHERE client_number_phone = %s
            """, (search_info,))
        print(cur.fetchall())

with psycopg2.connect(database="client", user="postgres", password="5240") as conn:
    with conn.cursor() as cur:
        create_table(cur)

conn.close()