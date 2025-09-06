# debug_create_tables.py
from sqlalchemy import inspect, text
from sqlalchemy.schema import CreateTable
from sqlalchemy import create_engine
import traceback

# import your app objects
import app.models as models_module   # ensures models are importable
from app.database import Base, engine

def print_banner(msg):
    print("\n" + "="*10 + " " + msg + " " + "="*10 + "\n")

def main():
    try:
        print_banner("Engine info")
        print("Engine URL:", engine.url)          # confirm the exact DB URL being used
        try:
            # enable SQL logging for this engine run (helps see DDL)
            engine.echo = True
        except Exception:
            pass

        # What SQLAlchemy metadata knows
        print_banner("SQLAlchemy metadata BEFORE create_all")
        print("metadata.tables keys:", list(Base.metadata.tables.keys()))

        # If the User class exists, show its Table object and CREATE statement
        User = getattr(models_module, "User", None)
        if User is None:
            print("models_module has NO 'User' attribute. Check app/models.py.")
        else:
            print("Found User model:", User)
            print("User.__table__:", User.__table__)
            # show DDL that SQLAlchemy would emit
            try:
                ddl = str(CreateTable(User.__table__).compile(engine))
                print("\nCreateTable DDL:\n", ddl)
            except Exception as e:
                print("Could not compile CreateTable:", e)

        # Attempt to create tables (will print SQL because engine.echo=True)
        print_banner("Calling Base.metadata.create_all(bind=engine)")
        Base.metadata.create_all(bind=engine)
        print("create_all() returned. Check below for inspector results.")

        # Inspect actual DB tables (public schema)
        inspector = inspect(engine)
        print_banner("Inspector: tables in DB (public schema)")
        try:
            tables = inspector.get_table_names(schema='public')
        except TypeError:
            # older/newer SQLAlchemy versions may ignore schema param
            tables = inspector.get_table_names()
        print("Tables in 'public' schema:", tables)

        # Check pg_tables for any 'users' row (Postgres)
        print_banner("Querying pg_tables for 'users'")
        with engine.connect() as conn:
            res = conn.execute(text("SELECT schemaname, tablename FROM pg_tables WHERE tablename='users'"))
            rows = res.fetchall()
            print("pg_tables rows:", rows)

        # Show final metadata keys AFTER create_all
        print_banner("SQLAlchemy metadata AFTER create_all")
        print("metadata.tables keys:", list(Base.metadata.tables.keys()))

        # Extra: show all schema names
        print_banner("Inspector: schema names")
        try:
            print("Schema names:", inspector.get_schema_names())
        except Exception as e:
            print("Could not get schema names:", e)

        print_banner("DONE")

    except Exception:
        print("Unhandled exception in debug script:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
