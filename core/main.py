import os
from extract import extract_nested_table_from_parent
from process import process_nested_tables_and_execute_commands
from save import save_updated_data_to_word


def main():
    input_file_path = input('Путь к файлу: ').strip()

    if not os.path.exists(input_file_path):
        print("Неверный путь")
        return

    nested_tables = extract_nested_table_from_parent(input_file_path)
    updated_tables = process_nested_tables_and_execute_commands(nested_tables)

    output_file_path = os.path.join(os.getcwd(), 'updated_testing.docx')

    save_updated_data_to_word(updated_tables, output_file_path)

    print(f"Результат сохранен в файл: {output_file_path}")


if __name__ == '__main__':
    main()
