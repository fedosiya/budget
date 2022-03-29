import databases
import asyncpg
import psycopg2

DATABASE_URL = "postgresql+psycopg2://postgres:1253480@localhost/mydb"
database = databases.Database(DATABASE_URL)
