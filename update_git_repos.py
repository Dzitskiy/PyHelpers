import os
import subprocess
import sys
from colorist import Color

def update_git_repos(base_dir):
    
    print(f"Set safe directory: {Color.CYAN}{base_dir}{Color.OFF}")
    try:
        subprocess.run(['git', 'config', '--global', '--add', 'safe.directory', '*'], check=True)
        print("Git 'safe.directory' setting updated successfully.")
    except subprocess.CalledProcessError as e:
        print("Error updating Git 'safe.directory' setting:")
        print(e)    

    for dir_name in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.isdir(dir_path):
            # Вывод названия каталога
            if os.path.exists(os.path.join(dir_path, '.git')):
                print(f"{Color.YELLOW}{dir_name}{Color.OFF}")

            else:
                print(dir_name)

            # Если это Git-репозиторий, обновляем его
            if os.path.exists(os.path.join(dir_path, '.git')):
                try:
                    os.chdir(dir_path)
                    subprocess.run(['git', 'checkout', 'master'], check=True)
                    subprocess.run(['git', 'pull'], check=True)
                    print(f"Updated repository: {Color.GREEN}{dir_name}{Color.OFF}")
                except subprocess.CalledProcessError as e:
                    print(f"Error updating repository: {Color.RED}{dir_name}{Color.OFF}")   
                    print(e)
                finally:
                    os.chdir(base_dir)

if __name__ == '__main__':
    # Получаем путь к каталогу из аргументов командной строки
    if len(sys.argv) > 1:
        base_directory = sys.argv[1]
    else:
        base_directory = os.getcwd()

    # Проверяем, существует ли указанный каталог
    if not os.path.exists(base_directory):
        print(f"{Color.RED}The specified directory does not exist: {base_directory}{Color.OFF}")               
        sys.exit(1)

    update_git_repos(base_directory)