import mysql.connector

def prepare_mysql_server():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='hbnb_dev',
            password='hbnb_dev_pwd'
        )

        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS hbnb_dev_db")

        cursor.execute("CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd'")

        cursor.execute("GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost'")

        cursor.execute("GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost'")

        connection.commit()

    except mysql.connector.Error as error:
        print(f"Error: {error}")

    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    prepare_mysql_server()
