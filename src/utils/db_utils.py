from sqlalchemy.engine import Engine
from sqlalchemy import text, MetaData, Table
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql
from typing import List
import pandas as pd



class PostgresUtils:
    def __init__(self, engine : Engine):
        self.engine = engine

    def get_tables_name(self, schema_name : str = 'public') -> List[str]:
        with self.engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = '{schema_name}'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result]
        return tables

        
    def get_table_schema(self, table_name : str) -> str:
        try:
            metadata =MetaData()
            table = Table(table_name, metadata, autoload_with=self.engine)
            ddl = CreateTable(table).compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True}
            )
            return str(ddl)
        except Exception as e:
            raise Exception(str(e))
        
    
    def get_all_tables_schema(self) -> dict:
        metadata = MetaData()
        metadata.reflect(bind=self.engine)

        schemas = {}

        for table_name, table in metadata.tables.items():
            ddl = CreateTable(table).compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True}
            )
            schemas[table_name] = str(ddl)

        return schemas
    
    
    def get_table_rows_md(self, table_name) -> str:
        query = text(f"""
            SELECT *
            FROM {table_name}
            LIMIT 5;
        """)

        df = pd.read_sql(query, engine)

        return df.to_markdown()
        

if __name__=="__main__":
    from sqlalchemy import URL, create_engine
    from src.utils import settings
    from src.edubot.prompts import agent

    db_user = settings.DB_USER
    db_pass = settings.DB_PASS
    db_host = settings.DB_HOST
    db_port = settings.DB_PORT
    db_name = settings.DB_NAME

    conn_url = URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        database=db_name
    )

    engine = create_engine(conn_url)
    pg_utils = PostgresUtils(engine=engine)

    doc = ""
    tables = pg_utils.get_tables_name()
    for name in tables:
        print(name)
        schema = pg_utils.get_table_schema(table_name=name)
        table = pg_utils.get_table_rows_md(table_name=name)
        doc += f"{agent.TEMPLATE.format(schema=schema, table=table)}"
    
    print(doc)

    path = settings.ROOT / "_docs" / "doc.md"
    with open(path, "w", encoding='utf-8') as f:
        f.write(doc)




"""
python3 -m src.utils.db_utils

"""