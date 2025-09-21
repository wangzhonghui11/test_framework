import yaml
import mysql.connector
from typing import Dict, List, Optional

class DBOperations:
    def __init__(self, env: str = "test"):
        self.config = self._load_config(env)
        self.conn = None

    def _load_config(self, env: str) -> Dict:
        with open("config/db_config.yaml") as f:
            configs = yaml.safe_load(f)
            return configs[env]

    def connect(self) -> bool:
        """创建数据库连接"""
        try:
            self.conn = mysql.connector.connect(**self.config)
            return True
        except mysql.connector.Error as err:
            print(f"连接错误: {err}")
            return False

    def close(self) -> None:
        """关闭数据库连接"""
        if self.conn and self.conn.is_connected():
            self.conn.close()

    def create_table(self) -> bool:
        """创建数据表"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE,
                        age INT
                    )
                """)
                self.conn.commit()
                return True
        except mysql.connector.Error as err:
            print(f"创建表错误: {err}")
            return False

    def insert_user(self, name: str, email: str, age: int) -> Optional[int]:
        """插入数据"""
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
                val = (name, email, age)
                cursor.execute(sql, val)
                self.conn.commit()
                return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"插入错误: {err}")
            return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """根据ID查询用户"""
        try:
            with self.conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"查询错误: {err}")
            return None

    def update_user(self, user_id: int, name: str, age: int) -> bool:
        """更新用户信息"""
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE users SET name = %s, age = %s WHERE id = %s"
                val = (name, age, user_id)
                cursor.execute(sql, val)
                self.conn.commit()
                return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"更新错误: {err}")
            return False

    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                self.conn.commit()
                return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"删除错误: {err}")
            return False

    def get_all_users(self) -> List[Dict]:
        """获取所有用户"""
        try:
            with self.conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users")
                return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"查询错误: {err}")
            return []