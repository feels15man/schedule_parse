import requests
import matplotlib.pyplot as plt
import numpy as np

Weekdays: tuple = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")


def main():
    # date = datetime.datetime.today()
    # date: str = "-".join(input("Дата (ДД.ММ.ГГ): ").split('.')[::-1])
    date = "-".join("2.4.2024".split('.')[::-1])

    # teacher:str = input("ФИО преподавателя: ").lower()
    teacher = "Писков Александр".lower()
    teacher_id: int = -1
    teachers_list = requests.get("https://ruz.spbstu.ru/api/v1/ruz/teachers/").json()['teachers']
    # pprint(teachers_list)
    for el in teachers_list:
        if teacher in el['full_name'].lower():
            teacher_id = el['id']
            teacher = el['full_name']
            break
    else:
        print("Такой преподаватель не найден")
        exit(-1)

    schedule = requests.get(f'https://ruz.spbstu.ru/api/v1/ruz/teachers/{teacher_id}/scheduler?date={date}').json()
    # pprint(schedule)
    print(f"\n{('Четная', 'Нечетная')[schedule['week']['is_odd']]} неделя"
          f" с {schedule['week']['date_start']} по {schedule['week']['date_end']}\n")

    lesson_counts: list[int] = [0] * 6

    for day in schedule['days']:
        print("-" * 50)
        print(f"{".".join(day['date'].split('-')[::-1])} {Weekdays[day['weekday'] - 1]}\n")
        lesson_counts[day['weekday'] - 1] = len(day['lessons'])
        for lesson in day['lessons']:
            print(f"  {lesson['time_start']} - {lesson['time_end']}\n"
                  f"  {lesson['subject']}\n"
                  f"  {lesson['typeObj']['name']}\n"
                  f"  {lesson['auditories'][0]['building']['name']} - {lesson['auditories'][0]['name']}\n"
                  f"  {teacher.title()}\n")

    print(lesson_counts)
    # plot
    plt.title("Schedule")
    plt.xlabel("days")
    plt.ylabel("lessons count")
    x_indexes = np.arange(6)
    y_indexes = np.arange(6)
    plt.xticks(x_indexes, Weekdays)
    plt.yticks(y_indexes, list(map(str, range(6))))

    plt.grid(axis='y')
    plt.bar(x_indexes, lesson_counts)

    plt.legend(["кол-во пар"])
    plt.show()


if __name__ == '__main__':
    main()
