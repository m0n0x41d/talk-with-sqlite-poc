import sqlite3
from typing import Literal

import loguru
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings

from text_to_sql_prompt import get_system_prompt

LOGGER = loguru.logger

DB1, DB2, DB3 = (
    "dbs/db1/db1.sqlite",
    "dbs/db2/db2.sqlite",
    "dbs/db3/db3.sqlite",
)
DB_IN_USE = DB3
LOGGER.info(f"Using DB: {DB_IN_USE}")

from os import getenv

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

OPENAI_API_KEY = SecretStr(getenv("OPENAI_API_KEY"))

model = OpenAIModel(
    model_name="gpt-4",
    provider=OpenAIProvider(api_key=OPENAI_API_KEY.get_secret_value()),
)


class SqlStrategy(BaseModel):
    do_i_have_tables_to_answer_this_question: bool
    table_to_query: list[str]
    columns_to_query: list[str]
    data_dependency: Literal["direct", "inderect", "N/A"]

    does_this_require_multiple_tables: bool
    does_this_require_subquery: bool
    does_this_require_recursive_query: bool


class SqlQuery(BaseModel):
    strategy: SqlStrategy
    query: str


sql_talk_agent = Agent(
    model,
    system_prompt=get_system_prompt(
        DB_IN_USE.replace(".sqlite", "_schema.md"),
    ),
    result_type=SqlQuery,
    model_settings=ModelSettings(temperature=0.0),
)


def get_db_connection(db_path: str):
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)


def execute_query(db_path: str, query: str):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


if __name__ == "__main__":
    while True:
        user_question = input(">: ")
        raw_model_response = sql_talk_agent.run_sync(user_question)
        LOGGER.info(f"Raw model response: {raw_model_response}")

        try:
            query_result = execute_query(DB_IN_USE, raw_model_response.data.query)
            LOGGER.info(f"Query result: {query_result}")
        except sqlite3.Error as e:
            LOGGER.error(f"SQLite error executing query: {e}")
            LOGGER.error(f"Failed query: {raw_model_response.data.query}")
