# PyHelpers


<details><summary> create_timesheet_template.py </summary>
</details>

<details><summary> update_git_repos.py </summary>

Скрипт для массого обновления Git-репозириев.

Пример вызова:
```bash
   python update_git_repos.py /path/to/directory
```
![image](https://github.com/user-attachments/assets/93f2a994-b6d1-498d-8f1a-d38574339158)

Скрипт импортирует необходимые модули: os для работы с файловой системой и subprocess для запуска команд в командной строке.

Может потребоваться установка colorist:
```bash
  pip install colorist
  pip install --upgrade colorist
```

Функция _update_git_repos()_, выполняет основную логику:
- Принимает путь к каталогу в качестве аргумента командной строки:
  - Если указанный каталог не существует, скрипт выводит ошибку и завершает выполнение.
  - Если параметр не передан, используется текущий рабочий каталог с помощью os.getcwd().
- Обновляет глобальную настройку Git safe.directory на значение '*', что позволит Git безопасно работать с любыми каталогами.
- Обходит все вложенния и определяет каталоги с помощью os.listdir(current_dir) и os.path.isdir(dir_path) - выводит их названия:
  - Если каталог является Git-репозиторием (содержит папку .git), то его название выделяется желтым цветом.
- Для всех вложенных Git-репозиториев выполняем:
  - Переход в каталог репозитория с помощью os.chdir(dir_path)
  - Переключение на ветку master с помощью subprocess.run(['git', 'checkout', 'master'], check=True).
  - Обновление репозитория с помощью subprocess.run(['git', 'pull'], check=True).
  - Вывод сообщения об обновлении в консоль:
    - Если возникает ошибка при выполнении команд Git - выводим сообщение об ошибке.

</details>
