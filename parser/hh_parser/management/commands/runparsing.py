from django.core.management.base import BaseCommand
import requests
from hh_parser.models import Requirements, Skill, Search


class Command(BaseCommand):
    def handle(self, *args, **options):
        # vacancy = input(f'Введите вакансию: ')
        # city = input(f'Введите город: ')
        vac_cit = (('python developer', 'Москва'), ('c++ developer', 'Москва'), ('Юрист', 'Москва'), ('Электрик', 'Москва'), ('Инженер', 'Москва'))
        for i in vac_cit:
            hh_parser(i[0], i[1])


def hh_parser(vacancy, city):

    #  Юзер-агент
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
              }

    #  url сайта
    url_vacancies = 'https://api.hh.ru/vacancies'

    # Ввод текста для поиска
    # vacancy = input(f'Введите вакансию/ии: ')
    # city = input(f'Введите город/а: ')

    vacancy_city = vacancy.lower().replace(' ', '') + ' AND ' + city

    #  Параметры запроса
    params = {'text': vacancy_city,
              'per_page': 50,
              'page': 1}

    # Запрос
    result = requests.get(url_vacancies, params=params, headers=headers).json()

    count_pages = result['pages']  # Количество страниц
    count = 0  # Количество найденных вакансий
    from_ = 0                    # Зарплата от и до
    to_ = 0
    c_f = 0  # Переменная для вычисления среднего значения зарплаты from
    c_t = 0  # Переменная для вычисления среднего значения зарплаты to
    requirements = {}  # Переменная для всех требуемых навыков
    best_skill = []  # Переменная для самых нужных навыков

    # Если вакансия и город не в базе, то ...
    if not Search.objects.filter(vacancy=vacancy, city=city).exists():

        want_pages = 4
        # while True:
        #     try:
        #         want_pages = int(input(f'Введите количество страниц, которые будут обрабатываться (всего{count_pages})'))  # Переменная определения кол-ва обрабатываемых страниц
        #         if 1 <= want_pages <= count_pages:
        #             break
        #     except: print(f'Вы ввели неверное значение')

        print(f'Обработка вакансий начата. Всего страниц: {want_pages}')

        # Получение средней зарплаты, количества вакансий, необходимых навыков для каждой страницы
        for i in range(1, want_pages + 1):
            print(f'Страница номер {i}')
            params = {'text': vacancy_city,
                      'per_page': 50,
                      'page': i}

            print(f'Получение страницы')
            # result = requests.get(url_vacancies, params=params, timeout=10).json()
            print(f'Выполнено!')

            print(f'Получение количества вакансий')
            count += result['found']  # Получение количества вакансий
            print(f'Выполнено!')

            print(f'Получение необходимых навыков и средней зарплаты')
            for item in result['items']:

                req_url = item['url']
                try:
                    req_result = requests.get(req_url, params=params, timeout=5).json()
                    try:
                        for name in req_result['key_skills']:
                            if name['name'].lower() not in requirements:
                                requirements[name['name'].lower()] = 1
                            else:
                                requirements[name['name'].lower()] += 1  # Получение необходимых навыков
                    except:
                        pass
                except:
                    pass

                try:
                    if item['salary']['from'] is not None:
                        from_ += item['salary']['from']
                        c_f += 1
                    if item['salary']['to'] is not None:
                        to_ += item['salary']['to']
                        c_t += 1
                except:
                    pass
            print(f'Выполнено!')

        try:
            from_ = int(from_ / c_f)  # Получение средней зарплаты

        except ZeroDivisionError:
            from_ = 'Нет информации'

        try:
            to_ = int(to_ / c_t)  # Получение средней зарплаты
        except ZeroDivisionError:
            to_ = 'Нет информации'

        # Получение несколько (5) самых нужных навыков
        try:
            requirements = dict(sorted(requirements.items(), key=lambda item: item[1]))
            best_skill.append(list(requirements)[:5])
            best_skill = best_skill[0]
        except:
            best_skill = 'Нет информации'

        # Вставить в search всё найденное

        Search.objects.create(vacancy=vacancy, city=city, count=count, sal_from=from_, sal_to=to_)

        # Если best_skill не пуст
        if best_skill:

            if best_skill != 'Нет информации':

                for skill in best_skill:
                    Skill.objects.create(name=skill)
                    # print(Search.objects.filter(vacancy=vacancy, city=city).values()[0])

                    w_id = Search.objects.filter(vacancy=vacancy, city=city).values()[0]['id']
                    s_id = Skill.objects.filter(name=skill).values()[0]['id']
                    # print(type(w_id), type(s_id))

                    Requirements.objects.create(world_id=w_id, skill_id=s_id)
            else:
                Skill.objects.create(name=best_skill)
                w_id = Search.objects.filter(vacancy=vacancy, city=city).values()[0]['id']
                s_id = Skill.objects.filter(name=best_skill).values()[0]['id']
                # print(w_id, s_id)
                Requirements.objects.create(world_id=w_id, skill_id=s_id)

        else:
            best_skill = 'Нет информации'

        return vacancy, city, count, from_, to_, best_skill

    # Если запрос в базе
    else:
        data = Search.objects.filter(vacancy=vacancy, city=city).values()[0]
        # print(data)

        # print(Requirements.objects.all().values())

        skill = []
        for d in Requirements.objects.all().values():
            id_s = d['skill_id']
            skill.append(Skill.objects.filter(id=id_s).values()[0]['name'])

        if not skill:
            skill = 'Нет информации'

        return data['vacancy'], data['city'], data['count'], data['sal_from'], data['sal_to'], skill
