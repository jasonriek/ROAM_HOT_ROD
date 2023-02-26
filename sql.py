import sqlite3

INTEGER = 'INTEGER'
TEXT = 'TEXT'
REAL = 'REAL'
BLOB = 'BLOB'

def formatToTableName(table_name:str):
    table_name = table_name.upper().strip()
    table_split = table_name.split()
    table_name = '_'.join(table_split)
    return table_name

class SQL:
    @staticmethod
    def createTable(table_name:str, columns:dict, db_path:str):
        '''Creates a table in the bids database.'''
        database = None
        try:
            tb_columns = ',\n'.join([f'{col_nm} {col_type}' for col_nm, col_type in columns.items()])
            sql = f'''
            CREATE TABLE IF NOT EXISTS {formatToTableName(table_name)}
            (id INTEGER PRIMARY KEY,
            {tb_columns}
            );
            '''
            database = sqlite3.connect(db_path) 
            cursor = database.cursor()
            cursor.execute(sql)
            database.commit()

        except Exception as error:
            print(f'SQL.createTable({table_name}, {columns}) Error: {str(error)}')
        finally:
            if database:
                database.close()

    @staticmethod
    def insert(table_name:str, data:dict, db_path:str):
        '''Inserts dictionary values in a specified table.
            EXAMPLE:
            
            data {
                "ITEM_ID": 25 # <column name>: <value>
            }
        '''
        database = None 
        sql = ''
        try:
            columns = list(data.keys())
            values = [data[column] for column in columns]
            columns_sql = ','.join(columns)
            values_sql = ','.join(['?' for _ in values])
            sql = f'INSERT INTO {table_name} ({columns_sql}) VALUES ({values_sql});'
            database = sqlite3.connect(db_path)
            cur = database.cursor()
            cur.execute(sql, values)
            database.commit()

        except Exception as error:
            print(f'SQL.insert({table_name}, {data}) Error: {str(error)}\n\nSQL: {sql}')
        
        finally:
            if database:
                database.close()

    @staticmethod
    def remove(table_name:str, cond_col:str, cond_val, db_path:str):
        '''Remove rows from a table where a column is equal to some value.'''
        database = None 
        try:
            sql = f'DELETE FROM {table_name} WHERE {cond_col} = ?;'
            database = sqlite3.connect(db_path)
            cursor = database.cursor()
            cursor.execute(sql, [cond_col])
            database.commit()
        except Exception as error:
            print(f'SQL.remove({table_name},{cond_col},{cond_val}) Error: {str(error)}')
        finally:
            if database:
                database.close()

    @staticmethod
    def update(table_name:str, col:str, val, cond_col:str, cond_val, db_path:str):
        '''Update some value from a table.'''
        con = None 
        try:
             sql = f'UPDATE {table_name} SET {col} = ? WHERE {cond_col} = ?;'
             con = sqlite3.connect(db_path)
             cursor = con.cursor()
             cursor.execute(sql, [val, cond_val])
             con.commit()

        except Exception as error:
            print(f'update({table_name}, {col}, {val}, {cond_col}, {cond_val}) Error: {str(error)}')
        finally:
            if con:
                con.close()
    
    @staticmethod
    def simpleUpdate(table_name:str, col:str, val, db_path:str):
        '''Update some value from a table.'''
        con = None 
        try:
             sql = f'UPDATE {table_name} SET {col} = ?;'
             con = sqlite3.connect(db_path)
             cursor = con.cursor()
             cursor.execute(sql, [val])
             con.commit()

        except Exception as error:
            print(f'update({table_name}, {col}, {val}) Error: {str(error)}')
        finally:
            if con:
                con.close()

    @staticmethod
    def value(table_name:str, col:str, cond_col:str, cond_val, db_path:str):
        '''A specific value from a table.'''
        database = None 
        value = None 
        try:
            sql = f'SELECT {col} FROM {table_name} WHERE {cond_col} = ?;'
            database = sqlite3.connect(db_path)
            cursor = database.cursor()
            value = cursor.execute(sql, [cond_val]).fetchone()
            if value:
                value = value[0] 
        except Exception as error:
            print(f'SQL.value({table_name}, {col}, {cond_col}, {cond_val}) Error: {str(error)}')
        finally:
            if database:
                database.close()
        return value        

    @staticmethod
    def getRow(table_name:str, item_id_column_name:str, item_id:str, db_path:str):
        '''Returns the values from a selected row based on the passed table name and item id.'''
        database = None 
        values = []
        try:
            sql = f'SELECT * FROM {table_name} WHERE {item_id_column_name} = ?;'
            database = sqlite3.connect(db_path)
            cursor = database.cursor()
            columns = cursor.execute(sql,[item_id]).fetchone()
            if columns:
                values =  [value for value in columns]
        except Exception as error:
            print(f'SQL.getRow({table_name}, {item_id}) Error: {str(error)}')
        finally:
            if database:
                database.close()
        return values

    @staticmethod
    def getColumn(table_name:str, column_name:str, db_path:str):
        '''Returns values from a selected column based on the passed table table name and column name.'''
        database = None 
        values = []
        try:
            sql = f'SELECT {column_name} FROM {table_name};'
            database = sqlite3.connect(db_path)
            cursor = database.cursor()
            values =  [row[0] for row in cursor.execute(sql).fetchall() if row]

        except Exception as error:
            print(f'SQL.getColumn({table_name}, {column_name}) Error: {str(error)}')
        
        finally:
            if database:
                database.close()
        return values       

    @staticmethod
    def tableNames(db_path:str):
        '''Returns a list containing all of the database's table names.'''
        database = None
        table_name_sql = ''
        table_names = []
        try:
            database = sqlite3.connect(db_path)
            cursor = database.cursor()
            table_name_sql = "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';"
            table_names = [table[0] for table in cursor.execute(table_name_sql).fetchall()]
        except Exception as error:
            print(f'SQL.tableNames({db_path}) Error: {str(error)}\n\nSQL: {table_name_sql}')
        finally:
            if database:
                database.close()
        return table_names
    
    @staticmethod
    def rowCount(table_name:str, db_path:str):
        '''Checks the table row count.'''
        database = None 
        count = 0
        try:
            database = sqlite3.connect(db_path)
            cursor = database.cursor()
            sql = f'SELECT COUNT(*) FROM {table_name};'
            count = int(cursor.execute(sql).fetchone()[0])
        except Exception as error:
            print(f'SQL.rowCount({table_name}, {db_path}) Error: {str(error)}')
        finally:
            if database:
                database.close()
        return count
