import requests
import argparse

# Ваш API ключ
API_KEY = ''

# URL API
url = 'https://leakcheck.io/api/v2/query'

# Функция для проверки утечек домена
def check_domain_leaks(domain):
    try:
        # Формируем URL с параметрами
        response = requests.get(f'{url}/{domain}?type=origin', headers={'X-API-Key': API_KEY})
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при проверке домена {domain}: {e}')
        return None

def main():
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Проверка утечек данных для указанного домена.')
    parser.add_argument('domain', type=str, help='Домен для проверки утечек')

    # Парсим аргументы
    args = parser.parse_args()
    domain_to_check = args.domain

    # Проверка домена
    result = check_domain_leaks(domain_to_check)
    if result:
        print(f'Результат проверки для домена {domain_to_check}:')
        print(f'Найдено результатов: {result["found"]}')
        
        # Сохраняем результаты в файл
        with open(f'{domain_to_check}_results.txt', 'w', encoding='utf-8') as file:
            file.write(f'Результат проверки для домена {domain_to_check}:\n')
            file.write(f'Найдено результатов: {result["found"]}\n\n')
            
            if result["found"] > 0:
                for entry in result["result"]:
                    # Выводим информацию о каждом найденном результате
                    email = entry.get("email")
                    username = entry.get("username")
                    password = entry.get("password")  # Если доступно

                    file.write(f'Email: {email}\n')
                    if username:
                        file.write(f'Username: {username}\n')
                    if password:
                        file.write(f'Password: {password}\n')
                    file.write('\n')  # Добавляем пустую строку между записями
            else:
                file.write('Утечек не найдено.\n')

if __name__ == '__main__':
    main()
