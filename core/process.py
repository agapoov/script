import subprocess


def del_dollar_sign(command):
    return command.lstrip("$ ").strip()


def process_nested_tables_and_execute_commands(nested_tables):
    updated_tables = []

    for table in nested_tables:
        updated_table = []
        for row in table:
            if len(row) >= 6:
                number, group, command, expected_value, yes, no = row
                command = del_dollar_sign(command)

                try:
                    result = subprocess.run(command, shell=True, text=True, capture_output=True)
                    output = result.stdout.strip()

                    if output == expected_value:
                        yes = '1'
                        no = ''
                    else:
                        yes = ''
                        no = '0'

                except Exception as e:
                    print(f"Ошибка при выполнении команды '{command}': {e}")
                    yes = '0'
                    no = '1'

                updated_row = [number, group, command, expected_value, yes, no]
                updated_table.append(updated_row)

        updated_tables.append(updated_table)

    return updated_tables
