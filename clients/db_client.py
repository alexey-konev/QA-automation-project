import os
import psycopg
from psycopg.rows import dict_row

class DatabaseClient:

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", 5432))
        self.dbname = os.getenv("DB_NAME", "qa_api_db")
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "postgres")

        self.connection = psycopg.connect(
            host=self.host,
            port=self.port,
            dbname = self.dbname,
            user = self.user,
            password = self.password,
            row_factory=dict_row
        )

        self.cursor = self.connection.cursor()

    def get_users(self):
        self.cursor.execute(
            """
            SELECT id, name, email
            FROM users
            """
        )

        return self.cursor.fetchall()

    def get_user_by_id(self, user_id):
        self.cursor.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        return self.cursor.fetchone()

    def get_user_by_email(self, email):
        self.cursor.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        return self.cursor.fetchone()

    def create_user(self, name, email):
        try:
            self.cursor.execute(
                """
                INSERT INTO users (name, email)
                VALUES (%s, %s)
                RETURNING id, name, email
                """,
                (name, email,)
            )

            self.connection.commit()

            return self.cursor.fetchone()

        except Exception:
            self.connection.rollback()
            raise


    def replace_user(self, user_id, name, email):
        try:
            self.cursor.execute(
                """
                UPDATE users
                SET name = %s,
                    email = %s
                WHERE id = %s
                RETURNING id, name, email;
                """,
                (name, email, user_id,)
            )

            self.connection.commit()

            return self.cursor.fetchone()

        except Exception:
            self.connection.rollback()
            raise

    def update_user(self, user_id, name=None, email=None):
        try:
            if name is not None and email is not None:
                self.cursor.execute(
                    """
                    UPDATE users
                    SET name = %s,
                        email = %s
                    WHERE id = %s
                    RETURNING id, name, email;
                    """,
                    (name, email, user_id)
                )

            elif name is not None:
                self.cursor.execute(
                    """
                    UPDATE users
                    SET name = %s
                    WHERE id = %s
                    RETURNING id, name, email;
                    """,
                    (name, user_id)
                )

            elif email is not None:
                self.cursor.execute(
                    """
                    UPDATE users
                    SET email = %s
                    WHERE id = %s
                    RETURNING id, name, email;
                    """,
                    (email, user_id)
                )

            else:
                return self.get_user_by_id(user_id)

            self.connection.commit()

            return self.cursor.fetchone()

        except Exception:
            self.connection.rollback()
            raise


    def delete_user(self, user_id):
        self.cursor.execute(
            """
            DELETE FROM users 
            WHERE id = %s
            RETURNING id, name, email
            """,
            (user_id,)
        )

        self.connection.commit()

        return self.cursor.fetchone()


    def close(self):
        self.cursor.close()
        self.connection.close()