import os

from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib import messages

from .models import Class, Pupil, Dish, DailyMenu, WeeklyBreakfasts
from django.contrib.auth.decorators import login_required


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

            week_start_date = datetime.now() - timedelta(days=datetime.now().weekday())

            weekly_breakfast, created = WeeklyBreakfasts.objects.get_or_create(
                pupil=pupil,
                week_start_date=week_start_date
            )

            for key, value in request.POST.items():
                if key.startswith('breakfast_'):
                    date_str = key.replace('breakfast_', '')
                    date = datetime.strptime(date_str, '%Y-%m-%d').date()

                    weekday = date.weekday()

                    if value and value != "none" and value != "":
                        dish = Dish.objects.get(id=value)
                        if weekday == 0:  # Понедельник
                            weekly_breakfast.monday = dish
                        elif weekday == 1:  # Вторник
                            weekly_breakfast.tuesday = dish
                        elif weekday == 2:  # Среда
                            weekly_breakfast.wednesday = dish
                        elif weekday == 3:  # Четверг
                            weekly_breakfast.thursday = dish
                        elif weekday == 4:  # Пятница
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

        today = datetime.now().date()
        current_weekday = today.weekday()
        if current_weekday >= 4:
            days_until_monday = (7 - current_weekday) % 7
            start_date = today + timedelta(days=days_until_monday)
            week_dates = [start_date + timedelta(days=i) for i in range(5)]
        else:
            week_dates = [today + timedelta(days=i - current_weekday) for i in range(current_weekday + 1, 5)]

        week_data = []
        for date in week_dates:
            try:
                menu = DailyMenu.objects.get(date=date)
                week_data.append({
                    'date': date,
                    'menu': menu,
                    'has_menu': True
                })
            except DailyMenu.DoesNotExist:
                week_data.append({
                    'date': date,
                    'menu': None,
                    'has_menu': False
                })

        context = {
            'today': today,
            'classes': classes,
            'week_data': week_data,
            'week_dates': week_dates
        }

        return render(request, 'pool.html', context)


def index(request: HttpRequest):
    return render(request, 'index.html')

