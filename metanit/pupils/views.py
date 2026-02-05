from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date
from django.http import HttpRequest
from django.contrib import messages

from .models import Class, Pupil, Dish, DailyMenu, WeeklyBreakfasts


def pooling(request: HttpRequest):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            class_id = request.POST.get('class_name')

            pupil, created = Pupil.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                class_group_id=class_id
            )

            # Обрабатываем выборы для обеих недель
            for key, value in request.POST.items():
                if key.startswith('breakfast_'):
                    date_str = key.replace('breakfast_', '')
                    breakfast_date = datetime.strptime(date_str, '%Y-%m-%d').date()

                    # Определяем начало недели для этой даты
                    week_start_date = breakfast_date - timedelta(days=breakfast_date.weekday())

                    # Получаем или создаем запись для этой недели
                    weekly_breakfast, created = WeeklyBreakfasts.objects.get_or_create(
                        pupil=pupil,
                        week_start_date=week_start_date
                    )

                    weekday = breakfast_date.weekday()

                    if value and value != "none" and value != "":
                        dish = Dish.objects.get(id=value)
                        if weekday == 0:
                            weekly_breakfast.monday = dish
                        elif weekday == 1:
                            weekly_breakfast.tuesday = dish
                        elif weekday == 2:
                            weekly_breakfast.wednesday = dish
                        elif weekday == 3:
                            weekly_breakfast.thursday = dish
                        elif weekday == 4:
                            weekly_breakfast.friday = dish
                    else:
                        # Сбрасываем выбор если "ничего"
                        if weekday == 0:
                            weekly_breakfast.monday = None
                        elif weekday == 1:
                            weekly_breakfast.tuesday = None
                        elif weekday == 2:
                            weekly_breakfast.wednesday = None
                        elif weekday == 3:
                            weekly_breakfast.thursday = None
                        elif weekday == 4:
                            weekly_breakfast.friday = None

                    weekly_breakfast.save()

            messages.success(request, f'Сохранены выборы для {first_name}!')
            return redirect('/pool/')

        except Exception as e:
            messages.error(request, f'Ошибка при сохранении: {str(e)}')
            return redirect('/pool/')

    else:
        dishes = Dish.objects.all().order_by('name')
        classes = Class.objects.all().order_by('name')

        today = date.today()
        current_weekday = today.weekday()

        # Определяем даты для двух недель
        if current_weekday >= 4:  # Пятница или позже
            # Показываем следующие две недели
            days_until_monday = (7 - current_weekday) % 7
            first_week_start = today + timedelta(days=days_until_monday)
        else:  # Понедельник-Четверг
            # Показываем оставшиеся дни текущей недели + следующая неделя
            first_week_start = today - timedelta(days=current_weekday)

        # Формируем список дат для двух недель (только рабочие дни)
        week_dates = []
        for week_offset in range(2):
            week_start = first_week_start + timedelta(days=week_offset * 7)
            for day_offset in range(5):  # Пн-Пт
                day_date = week_start + timedelta(days=day_offset)
                # Добавляем только будущие даты (включая сегодня)
                if day_date >= today:
                    week_dates.append(day_date)

        # Группируем данные по неделям
        weeks_data = []
        current_week_dates = []
        current_week_data = []
        current_week_start = None

        for breakfast_date in week_dates:
            week_start = breakfast_date - timedelta(days=breakfast_date.weekday())

            # Если началась новая неделя
            if current_week_start != week_start:
                # Сохраняем предыдущую неделю
                if current_week_dates:
                    weeks_data.append({
                        'week_start': current_week_start,
                        'week_number': len(weeks_data) + 1,
                        'dates': current_week_dates,
                        'data': current_week_data
                    })

                current_week_start = week_start
                current_week_dates = []
                current_week_data = []

            # Добавляем день в текущую неделю
            try:
                menu = DailyMenu.objects.get(date=breakfast_date)
                current_week_data.append({
                    'date': breakfast_date,
                    'menu': menu,
                    'has_menu': True
                })
            except DailyMenu.DoesNotExist:
                current_week_data.append({
                    'date': breakfast_date,
                    'menu': None,
                    'has_menu': False
                })

            current_week_dates.append(breakfast_date)

        # Добавляем последнюю неделю
        if current_week_dates:
            weeks_data.append({
                'week_start': current_week_start,
                'week_number': len(weeks_data) + 1,
                'dates': current_week_dates,
                'data': current_week_data
            })

        context = {
            'today': today,
            'classes': classes,
            'weeks_data': weeks_data,
            'week_dates': week_dates
        }

        return render(request, 'pool.html', context)


def index(request: HttpRequest):
    return render(request, 'index.html')