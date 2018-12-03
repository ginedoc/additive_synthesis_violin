from table import table

if __name__ == "__main__":
    table = table()
    if not table.is_table_exist():
        table.build_table()
        table.save_table()
        
