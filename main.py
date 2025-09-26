import os
import shlex
import re
from typing import List


class ShellEmulator:
    def __init__(self):
        self.vfs_name = "myvfs"
        self.running = True
        self.current_dir = os.getcwd()

    def get_env_var(self, var_name: str) -> str:
        """Получает значение переменной окружения"""
        if var_name == "HOME":
            return os.environ.get("HOME") or os.environ.get("USERPROFILE", "")
        elif var_name == "USER":
            return os.environ.get("USER") or os.environ.get("USERNAME", "")
        else:
            return os.environ.get(var_name, "")

    def expand_variables(self, text: str) -> str:
        """Раскрывает переменные окружения в тексте"""

        def replace_var(match):
            var_name = match.group(1) or match.group(2)
            return self.get_env_var(var_name)

        # Регулярное выражение для поиска ${VAR} и $VAR
        pattern = r'\$\{([^}]+)\}|\$([a-zA-Z_][a-zA-Z0-9_]*)'
        return re.sub(pattern, replace_var, text)

    def parse_command(self, input_line: str) -> List[str]:
        """Парсит команду с раскрытием переменных"""
        try:
            # Сначала раскрываем переменные
            expanded_line = self.expand_variables(input_line)
            # Затем разбиваем на аргументы
            return shlex.split(expanded_line)
        except ValueError as e:
            print(f"Ошибка парсинга: {e}")
            return []

    def execute_command(self, command: str, args: List[str]):
        """Выполняет команду"""
        if command == "exit":
            self.running = False
            print("Выход из эмулятора")

        elif command == "ls":
            print(f"Команда: ls, Аргументы: {args}")
            # Заглушка - просто выводим информацию
            print("drwxr-xr-x 2 user user 4096 Jan 1 00:00 dir1")
            print("-rw-r--r-- 1 user user 1024 Jan 1 00:00 file1.txt")

        elif command == "cd":
            print(f"Команда: cd, Аргументы: {args}")
            if not args:
                print("cd: missing argument")
            else:
                print(f"Изменение директории на: {args[0]}")

        elif command == "echo":
            # Реализуем команду echo
            if args:
                print(' '.join(args))
            else:
                print()

        elif command == "":
            # Пустая команда - ничего не делаем
            pass

        else:
            print(f"{command}: command not found")

    def run(self):
        """Основной цикл REPL"""
        print("Добро пожаловать в эмулятор командной строки!")
        print("Введите 'exit' для выхода")
        print("-" * 50)
        print("Доступные переменные окружения:")
        print(f"  HOME/USERPROFILE = {self.get_env_var('HOME')}")
        print(f"  USER/USERNAME = {self.get_env_var('USER')}")
        print("-" * 50)

        while self.running:
            try:
                # Показываем приглашение с именем VFS
                current_dir_name = os.path.basename(self.current_dir)
                prompt = f"{self.vfs_name}:/{current_dir_name}$ "
                input_line = input(prompt).strip()

                # Парсим команду
                parts = self.parse_command(input_line)
                if not parts:
                    continue

                # Извлекаем команду и аргументы
                command = parts[0]
                args = parts[1:]

                # Выполняем команду
                self.execute_command(command, args)

            except KeyboardInterrupt:
                print("\nДля выхода введите 'exit'")
            except EOFError:
                print("\nВыход")
                break

def main():
    """Точка входа в приложение"""
    shell = ShellEmulator()
    shell.run()

if __name__ == "__main__":
    main()
