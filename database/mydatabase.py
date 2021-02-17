from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

SQLITE                  = 'sqlite'
# MYSQL                   = 'mysql'
# POSTGRESQL              = 'postgresql'

# Table Names
RECENT = 'recent'
# CONSTANTS = 'constants'


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        # MYSQL: 'mysql://user@localhost/{DB}',
        # POSTGRESQL: 'postgresql://user@localhost/{DB}',
    }

    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)

            self.db_engine = create_engine(engine_url)
            print(self.db_engine)

        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        recent = Table(RECENT, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('search_key', String)
                      )
        # constants = Table(CONSTANTS, metadata,
        #                 Column('key', String, primary_key=True),
        #                 Column('value', String)
        #                 )

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '' : return

        print (query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)


    def print_recent_data(self, search=''):
        
        if not search:
            return 'No keyword given to search'
        else:
            query = "SELECT search_key FROM '{}' WHERE search_key LIKE '%{}%';".format(RECENT, search)

        print(query)

        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                result_str = []
                for item in result:
                  result_str.append(item[0])
                result.close()
                return ", ".join(result_str)

    def insert_to_recent(self, search):
        query = "INSERT INTO {}(search_key) " \
                        "VALUES ('{}');".format(RECENT, search)
        
        self.execute_query(query)
