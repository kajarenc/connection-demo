import streamlit as st
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

st.title("Demo using psycopg3 and psycopg_pool!")

with st.echo(code_location="below"):

    @st.experimental_singleton
    def get_connection_pool():
        pool = ConnectionPool(
            conninfo="postgres://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs",
            min_size=1,
            max_size=2,
        )
        print("Connection pool created successfully using PostgreSQL")
        return pool

    clear_memo_cache = st.button("Clear cache")

    if clear_memo_cache:
        st.experimental_memo.clear()

    @st.experimental_memo
    def get_data(limit):
        pool = get_connection_pool()
        pool.check()

        with pool.connection(timeout=4) as conn:
            print(f"Connection ID: {id(conn)}, {conn}")
            with conn.cursor(row_factory=dict_row) as curs:
                curs.execute(
                    "SELECT * FROM rnc_database ORDER BY id LIMIT %s", (limit,)
                )
                data = curs.fetchall()
                print("Data fetched successfully")
        return data

    limit = st.number_input("Limit", min_value=10, max_value=50, value=10, step=10)
    my_data = get_data(limit=limit)
    st.dataframe(my_data)
