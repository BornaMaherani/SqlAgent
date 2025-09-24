import os
import urllib

import prettytable
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

# Load environment variables first
load_dotenv()

# Import settings after environment variables are loaded
from config import settings
def connect_llm(api_key, model="deepseek/deepseek-chat-v3.1:free"):
    """
    Initialize and return a ChatOpenAI LLM instance.
    """
    try:
        return ChatOpenAI(
            temperature=0,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model=model
        )
    except Exception as e:
        print(f"\n\n*****  LLM Connection Failed: <<<{e}>>>  *****\n\n")

def connect_db():
    """
    Establish and return a connection to the local SQL Server database.
    """
    try:
        params = urllib.parse.quote_plus(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=localhost;"
            "Database=grocery;"
            "Trusted_Connection=yes;"
        )
        connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
        return SQLDatabase.from_uri(connection_string)
    except Exception as e:
        print(f"\n\n*****  Failed Connecting to the 'grocery' DataBase: <<<{e}>>>  *****\n\n")


def print_table(column_names, rows):
    """
    Print query results in a formatted table using PrettyTable.
    """
    table = prettytable.PrettyTable(column_names)
    table._set_padding_width(1)
    for row in rows:
        table.add_row(row if not isinstance(row, dict) else list(row.values()))
    return table
