from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_xatmusers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS xatmusers (
        id BIGINT PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        poralar varchar(25500) NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_xatmuser(self, id, full_name, poralar):
        sql = "INSERT INTO xatmusers (id, full_name, poralar) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, id, full_name, poralar, fetchrow=True)

    async def select_all_xatmusers(self):
        sql = "SELECT * FROM xatmusers"
        return await self.execute(sql, fetch=True)

    async def select_xatmuser(self, **kwargs):
        sql = "SELECT * FROM xatmusers WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_user_s(self):
        sql = "SELECT COUNT(*) FROM xatmusers"
        return await self.execute(sql, fetchval=True)

    async def update_user_poralar(self, username, telegram_id):
        sql = "UPDATE xatmusers SET poralar=$1 WHERE id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def select_xatmdagi_user(self, **kwargs):
        sql = "SELECT * FROM xatmusers WHERE NOT "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def delete_xatmusers(self):
        await self.execute("DELETE FROM xatmusers WHERE TRUE", execute=True)

    async def drop_xatmusers(self):
        await self.execute("DROP TABLE xatmusers", execute=True)

    async def create_table_xatm_db(self):
        sql = """
        CREATE TABLE IF NOT EXISTS xatm_db (
        id INT PRIMARY KEY,
        list VARCHAR(25500) NOT NULL,
        xatm_data varchar(25500)
        );
        """
        await self.execute(sql, execute=True)

    async def add_xatm_db(self, id, list, xatm_data):
        sql = "INSERT INTO xatm_db (id, list, xatm_data) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, id, list, xatm_data, fetchrow=True)

    async def select_all_xatms(self):
        sql = "SELECT * FROM xatm_db ORDER BY id"
        return await self.execute(sql, fetch=True)

    async def select_xatms(self):
        sql = "SELECT list FROM xatm_db"
        return await self.execute(sql, fetch=True)

    async def select_user_xatms(self, **kwargs):
        sql = "SELECT * FROM xatm_db WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM xatm_db"
        return await self.execute(sql, fetchval=True)

    async def update_user_xatm_data(self, xatm_data, id):
        sql = "UPDATE xatm_db SET xatm_data=$1 WHERE id=$2"
        return await self.execute(sql, xatm_data, id, execute=True)

    async def update_user_xatm_list(self, list, id):
        sql = "UPDATE xatm_db SET list=$1 WHERE id=$2"
        return await self.execute(sql, list, id, execute=True)

    async def delete_users_xatms(self):
        await self.execute("DELETE FROM xatm_db WHERE TRUE", execute=True)

    async def drop_table_xatm_db(self):
        await self.execute("DROP TABLE xatm_db", execute=True)

    async def select_last_xatm(self):
        sql = "SELECT * FROM xatm_db ORDER BY id DESC LIMIT 1"
        return await self.execute(sql, fetchrow=True)

    async def delete_xatm(self, id):
        await self.execute("DELETE FROM xatm_db WHERE id=$1", id, execute=True)

    async def create_table_stat(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users_stat (
        id BIGINT NOT NULL UNIQUE,
        fullname VARCHAR(255) NOT NULL,
        poralar_soni BIGINT,
        xatmonalar_soni BIGINT 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_users_stat(self, id, fullname, poralar_soni, xatmonalar_soni):
        sql = "INSERT INTO users_stat (id, fullname, poralar_soni, xatmonalar_soni) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, id, fullname, poralar_soni, xatmonalar_soni, fetchrow=True)

    async def select_users_stat(self, **kwargs):
        sql = "SELECT * FROM users_stat WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_all_stat(self):
        sql = "SELECT * FROM users_stat ORDER BY id"
        return await self.execute(sql, fetch=True)

    async def delete_users_stat(self):
        await self.execute("DELETE FROM users_stat WHERE TRUE", execute=True)

    async def drop_table_users_stat(self):
        await self.execute("DROP TABLE users_stat", execute=True)

    async def update_stat_users_poralar(self, poralar_soni, id):
        sql = "UPDATE users_stat SET poralar_soni=$1 WHERE id=$2"
        return await self.execute(sql, poralar_soni, id, execute=True)

    async def update_stat_users_xatms(self, xatmonalar_soni, id):
        sql = "UPDATE users_stat SET xatmonalar_soni=$1 WHERE id=$2"
        return await self.execute(sql, xatmonalar_soni, id, execute=True)

    async def update_stat_users_fname(self, poralar_soni, id):
        sql = "UPDATE users_stat SET fullname=$1 WHERE id=$2"
        return await self.execute(sql, poralar_soni, id, execute=True)

    async def count_all_users_stat(self):
        sql = "SELECT COUNT(*) FROM users_stat"
        return await self.execute(sql, fetchval=True)

    async def create_table_backporalar(self):
        sql = """
        CREATE TABLE IF NOT EXISTS backporalar_db(
        id INT PRIMARY KEY,
        backcolumn VARCHAR(25500)
        );
        """

    async def add_backporalar(self, id, backcolumn):
        sql = "INSERT INTO backporalar_db(id, backcolumn) VALUES ($1, $2) returning *"
        return await self.execute(sql, id, backcolumn, fetchrow=True)

    async def delete_row_backporalar(self):
        await self.execute("DELETE FROM backporalar_db WHERE TRUE", execute=True)