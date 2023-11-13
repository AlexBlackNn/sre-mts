def transfer_dataset(sqlite, postgres):
    for Table in config.TABLE:
        table = Table()
        for sql_tables_data in sqlite.generator_data_for_postgres(
                table, arraysize=10000
        ):
            logger.info(
                f'GENERATOR transfer data from '
                f'{table.sqlite_name_table} to {table.postgres_name_table}'
            )
            s_template, name_template = table.create_template()
            postgres.load_data(
                sql_tables_data,
                table.postgres_name_table,
                s_template,
                name_template
            )