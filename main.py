import random

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation


def get_schoolkid(name):
    if not name:
        print('Не передано имя ученика!')
        return
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.DoesNotExist:
        print(f'Ученик {name} отсутствует в списках!')
        return
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено больше одного ученика! Уточните запрос!')
        return


def fix_marks(name):
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return
    Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    ).update(points=5)
    print(f'Оценки ученика {name} исправлены!')


def remove_chastisements(name):
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return
    Chastisement.objects.filter(schoolkid=schoolkid).delete()
    print(f'Замечания ученика {name} удалены!')


def create_commendation(name, lesson_name):
    commendations = [
        "Молодец!",
        "Отлично!",
        "Хорошо!",
        "Гораздо лучше, чем я ожидал!",
        "Ты меня приятно удивил!",
        "Великолепно!",
        "Прекрасно!",
        "Ты меня очень обрадовал!",
        "Именно этого я давно ждал от тебя!",
        "Сказано здорово – просто и ясно!",
        "Ты, как всегда, точен!",
        "Очень хороший ответ!",
        "Талантливо!",
        "Ты сегодня прыгнул выше головы!",
        "Я поражен!",
        "Уже существенно лучше!",
        "Потрясающе!",
        "Замечательно!",
        "Прекрасное начало!",
        "Так держать!",
        "Ты на верном пути!",
        "Здорово!",
        "Это как раз то, что нужно!",
        "Я тобой горжусь!",
        "С каждым разом у тебя получается всё лучше!",
        "Мы с тобой не зря поработали!",
        "Я вижу, как ты стараешься!",
        "Ты растешь над собой!",
        "Ты многое сделал, я это вижу!",
        "Теперь у тебя точно все получится!",
    ]
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=lesson_name
    ).order_by('?').first()
    if not lesson:
        print(f'Предмет {lesson_name} не найден! Уточните предмет!')
        return
    Commendation.objects.create(
        text=random.choice(commendations),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
    print('Похвала добавлена! Теперь ты еще больший молодец!')
