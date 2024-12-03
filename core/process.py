import subprocess
import re

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'


def remove_comments_for_3(text):
    comment_match = re.search(r'\s*\(.*\)', text)
    comment = comment_match.group(0) if comment_match else ''
    cleaned_text = re.sub(r'\s*\(.*\)', '', text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text, comment


def parse_output(output):
    output_dict = {}
    lines = output.strip().split("\n")

    for line in lines:
        parts = line.split("=")
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            output_dict[key] = value
    return output_dict


def del_dollar_sign(command):
    return command.lstrip("$ ").strip()


def check_greater_or_equal(value, expected_value, comment):
    try:
        value = float(value)
        expected_value = float(expected_value)
    except ValueError:
        pass

    if 'больше' in comment or 'или больше' in comment:
        return value >= expected_value
    else:
        return value == expected_value


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
                    if number.startswith('3'):
                        clear_expected_value, comment = remove_comments_for_3(expected_value)

                        output_dict = parse_output(output)
                        expected_dict = parse_output(clear_expected_value)

                        match_found = False
                        for key, expected in expected_dict.items():
                            if key in output_dict:
                                if check_greater_or_equal(output_dict[key], expected, comment):
                                    match_found = True
                                    break

                        if match_found:
                            yes = '1'
                            no = ''
                        else:
                            yes = ''
                            no = '0'

                    else:
                        if output == expected_value:
                            yes = '1'
                            no = ''
                        else:
                            yes = ''
                            no = '0'

                    if yes == '1':
                        print(f'{GREEN}Processed for {number}, match: {yes == "1"}{RESET}')
                    else:
                        print(f'{RED}Processed for {number}, match: {yes == "1"}{RESET}')

                except Exception as e:
                    print(f"{RED}Ошибка при выполнении команды '{command}': {e}{RESET}")

                    yes = 'Error'
                    no = 'Error'

                updated_row = [number, group, command, expected_value, yes, no]
                updated_table.append(updated_row)

        updated_tables.append(updated_table)

    return updated_tables
