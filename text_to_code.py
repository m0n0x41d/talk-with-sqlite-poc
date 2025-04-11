# DO NOT USE THIS CODE IN PRODUCTION.
# YOU SHOULD SECURE ENVIRONMENT WHERE YOU ALLOWING LLM TO RUN ANY CODE MUCH BETTER!
import sqlite3
from os import getenv
from typing import Literal

import loguru
from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings

from prompts import text_to_code_system_prompt

LOGGER = loguru.logger

DB1 = "dbs/db1/db1.sqlite"
LOGGER.info(f"Using DB: {DB1}")


load_dotenv()

OPENAI_API_KEY = SecretStr(getenv("OPENAI_API_KEY", "NO_KEY_SET_IT_IN_DOT_ENV"))

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

    do_i_have_all_the_python_libraries_that_i_need: bool
    which_libraries_do_i_need_but_dont_have: list[str]


class FinalResponse(BaseModel):
    response_type: Literal["code", "table"]
    content: str


class SqlQuery(BaseModel):
    strategy: SqlStrategy
    response: FinalResponse


sql_talk_agent = Agent(
    model,
    system_prompt=text_to_code_system_prompt(
        DB1.replace(".sqlite", "_schema.md"),
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

        match raw_model_response.data.response.response_type:
            case "code":
                code_to_execute = raw_model_response.data.response.content
                code_to_execute = code_to_execute.replace("DATABASE_PATH", f'"{DB1}"')
                print("This is the code I'm going to execute:")
                print(code_to_execute)
                ok = input("Execute the code? (y/n) ")
                if ok.lower() not in ["y", "yes", "ok", "okay"]:
                    LOGGER.info("Code not executed")
                    continue
                LOGGER.info(f"Executing generated code:\\n{code_to_execute}")
                try:
                    exec(code_to_execute, globals())
                except Exception as e:
                    LOGGER.error(f"Error executing generated code: {e}")
            case "table":
                table_to_display = raw_model_response.data.response.content
                print(table_to_display)
