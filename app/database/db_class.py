"""
Здесь класс БД
"""
import os
import psycopg2
from typing import Any
from psycopg2._psycopg import cursor, connection
from dotenv import load_dotenv
from .db_base_class import BaseDatabase
from dataclasses import dataclass

load_dotenv()

class  Database(BaseDatabase):
    def __init__(self) -> None:
        """
        Инициализирует БД. 
        НЕ МЕНЯЙТЕ НАЗВАНИЕ СХЕМЫ public на другое!!!
        """
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_PORT = os.getenv("DB_INTERNAL_PORT")

        self.init_QUERY = """
        CREATE SCHEMA IF NOT EXISTS public;

        CREATE TABLE IF NOT EXISTS sc_groups (
        id SERIAL PRIMARY KEY,
        title TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS sc_prep (
        id SERIAL PRIMARY KEY,
        fio TEXT NOT NULL UNIQUE,
        chair TEXT,
        degree TEXT,
        photo TEXT,
        student_id INTEGER,
        archive BOOL DEFAULT 'f'
        );

        CREATE TABLE IF NOT EXISTS sc_disc (
        id SERIAL PRIMARY KEY,
        title TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS sc_rasp (
        id SERIAL PRIMARY KEY,
        disc_id INTEGER REFERENCES sc_disc(id),    
        prep_id INTEGER REFERENCES sc_prep(id),
        weekday INTEGER,
        week INTEGER,
        lesson INTEGER,
        group_id INTEGER REFERENCES sc_groups(id),
        subgroup INTEGER
        );
        """
        try:
            conn, cur = self.set_conn()
            cur.execute(self.init_QUERY)
        except (Exception, psycopg2.Error) as error:
            conn = None
            print("PostgreSQL error occured", error)
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")

    def set_conn(self) -> tuple[connection, cursor]:
        try:
            conn = psycopg2.connect(
                database=self.DB_NAME,
                user=self.DB_USER,
                host=self.DB_HOST,
                port=self.DB_PORT,
                password=self.DB_PASSWORD   
            )
            cur = conn.cursor()
        except:
            conn, cur = (None, None)
        finally:
            return conn, cur

    def reset_data(self):
        """
        Удаляет все записи в БД. 
        НЕ МЕНЯЙТЕ НАЗВАНИЕ СХЕМЫ public на другое!!!
        """
        QUERY = "DROP SCHEMA public CASCADE;" + " " + self.init_QUERY
        try:
            conn, cur = self.set_conn()
            cur.execute(QUERY)
        except (Exception, psycopg2.Error) as error:
            print("PostgreSQL error occured", error)
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")

    def set_data(self, query: str, *args):
        try:
            conn, cur = self.set_conn()
            cur.execute(query, (args))
        except (Exception, psycopg2.Error) as error:
            print("PostgreSQL error occured", error)
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")
            
    def get_data(self, query: str, *args) -> Any:
        try:
            conn, cur = self.set_conn()
            response = cur.execute(query, (args))
        except (Exception, psycopg2.Error) as error:
            print("PostgreSQL error occured", error)
        finally:
            if conn:
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")
                return response
                
    def set_rasp(self, disc: str, prep: str, group: str, weekday: int, week: int = None, 
                 lesson: int = None, subgroup: int = None):
        QUERY = """
        INSERT INTO 
            sc_rasp (disc_id, prep_id, weekday, week, lesson, group_id, subgroup)
        SELECT
            (SELECT id FROM sc_disc WHERE sc_disc.title = %s),
            (SELECT id FROM sc_prep WHERE sc_prep.fio = %s),
            %s, 
            %s, 
            %s,
            (SELECT id FROM sc_groups WHERE sc_groups.title = %s),
            %s;
        """
        self.set_data(QUERY, disc, prep, weekday, week, lesson, group, subgroup)

    def set_prep(self, fio: str, chair: str = None, degree: str = None, photo: str = None,
                student_id: int = None, archive: bool = False):
        QUERY = """
        INSERT INTO 
            sc_prep (fio, chair, degree, photo, student_id, archive)
        VALUES
            (%s, %s, %s, %s, %s, %s);
        """
        self.set_data(QUERY, fio, chair, degree, photo, student_id, archive)

    def set_group(self, title: str):
        QUERY = """
        INSERT INTO 
            sc_groups (title)
        VALUES
            (%s);
        """
        self.set_data(QUERY, title)

    def set_subj(self, title: str):
        QUERY = """
        INSERT INTO 
            sc_disc (title)
        VALUES
            (%s);
        """
        self.set_data(QUERY, title)

    