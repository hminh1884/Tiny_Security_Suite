import mysql.connector
import bcrypt
import os
import json
import re

from datetime import datetime, timedelta

class AuthService:
    DB_CONFIG = {
        "host": "localhost",
        "user": "root",       
        "password": "",       
        "database": "tiny_security_db",
        "port": 3307
    }
    
    SESSION_FILE = "logs/session.json"

    @classmethod
    def _get_connection(cls):
        return mysql.connector.connect(**cls.DB_CONFIG)

    @classmethod
    def register(cls, email: str, password: str) -> bool:
        if not email or not password or cls.is_temp_mail(email):
            return False
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            password_bytes = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

            query = "INSERT INTO users (email, password_hash, last_active) VALUES (%s, %s, NOW())"
            cursor.execute(query, (email, hashed_password))
            conn.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close() ; conn.close()

    @classmethod
    def login(cls, email: str, password: str) -> bool:
        if not email or not password:
            return False
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            query = "SELECT password_hash FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                cursor.execute("UPDATE users SET last_active = NOW() WHERE email = %s", (email,))
                conn.commit()
                return True
            return False
        except mysql.connector.Error:
            return False
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close() ; conn.close()

    @classmethod
    def update_activity(cls, email: str):
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET last_active = NOW() WHERE email = %s", (email,))
            conn.commit()
        except mysql.connector.Error:
            pass
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close() ; conn.close()

    @classmethod
    def check_session_timeout(cls, email: str) -> bool:
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT last_active FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            
            if result and result[0]:
                last_active = result[0]
                if datetime.now() - last_active > timedelta(days=30):
                    return True 
            return False
        except mysql.connector.Error:
            return True
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close() ; conn.close()

    @classmethod
    def save_local_session(cls, email: str):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        with open(cls.SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump({"logged_in_user": email}, f)

    @classmethod
    def get_local_session(cls) -> str:
        if os.path.exists(cls.SESSION_FILE):
            try:
                with open(cls.SESSION_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("logged_in_user", "")
            except Exception:
                return ""
        return ""

    @classmethod
    def clear_local_session(cls):
        if os.path.exists(cls.SESSION_FILE):
            os.remove(cls.SESSION_FILE)

    @classmethod
    def set_password(cls, email: str, new_password: str):
        try:
            conn = cls._get_connection()
            cursor = conn.cursor()
            password_bytes = new_password.encode('utf-8')
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
            cursor.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_password, email))
            conn.commit()
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close() ; conn.close()

    @staticmethod
    def is_temp_mail(email: str) -> bool:
        domain = email.split("@")[-1].lower().strip() if "@" in email else ""
        temp_mail_blacklist = {"10minutemail.com", "yopmail.com", "mailinator.com"}
        return domain in temp_mail_blacklist or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    
    @staticmethod
    def generate_email_otp() -> str:
        import random
        import string
        return "".join(random.choice(string.digits) for _ in range(6))

    @classmethod
    def send_verification_email(cls, recipient_email: str, otp_code: str):
       
        pass