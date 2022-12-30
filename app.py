import streamlit as st
from psycopg_pool import ConnectionPool

st.title("DEMO TIME!")


@st.experimental_singleton
def get_connection_pool():
    pool = ConnectionPool(
        conninfo="postgresql://myuser:mypass@localhost:5432/thedatabase",
        min_size=1,
        max_size=2,
    )
    print(f"Connection pool created successfully using postgreSQL")
    return pool


clear_memo_cache = st.button("Clear cache")

if clear_memo_cache:
    st.experimental_memo.clear()


@st.experimental_memo
def get_data(limit=4):
    pool = get_connection_pool()
    with pool.connection(timeout=4) as conn:
        print(f"CONNECTION ID: {id(conn)}, {conn}")
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM movies ORDER BY id LIMIT %s", (limit,))
            data = curs.fetchall()
            print(f"Data fetched successfully")
    return data


limit = st.number_input("Limit", min_value=1, max_value=10, value=4)

my_data = get_data(limit=limit)

st.table(my_data)
