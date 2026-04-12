from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_GET

from .models import Class, Pupil, Dish, DailyMenu, WeeklyBreakfasts


def _get_current_week_start():
    """Возвращает дату начала текущей/ближайшей активной недели (как в pooling GET)."""
    today = date.today()
    current_weekday = today.weekday()
    if current_weekday >= 4:  # Пятница или позже — показываем следующую неделю
        days_until_monday = (7 - current_weekday) % 7
        first_week_start = today + timedelta(days=days_until_monday)
    else:
        first_week_start = today - timedelta(days=current_weekday)
    return first_week_start


@require_GET
def check_pupil(request: HttpRequest):
    """
    AJAX-endpoint: проверяет, есть ли уже заявка для ученика на текущие недели.
    Возвращает JSON с информацией о существующих выборах.
    """
    first_name = request.GET.get('first_name', '').strip()
    last_name = request.GET.get('last_name', '').strip()
    class_id = request.GET.get('class_id', '').strip()

    if not (first_name and last_name and class_id):
        return JsonResponse({'found': False})

    try:
        pupil = Pupil.objects.get(
            first_name=first_name,
            last_name=last_name,
            class_group_id=class_id
        )
    except Pupil.DoesNotExist:
        return JsonResponse({'found': False})

    first_week_start = _get_current_week_start()
    second_week_start = first_week_start + timedelta(days=7)

    DAY_NAMES = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт']

    existing_weeks = []
    for week_start in [first_week_start, second_week_start]:
        try:
            wb = WeeklyBreakfasts.objects.get(pupil=pupil, week_start_date=week_start)
            days = []
            for attr, day_name in zip(
                ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
                DAY_NAMES
            ):
                dish = getattr(wb, attr)
                days.append({
                    'day': day_name,
                    'dish': dish.short_name if dish else '—'
                })
            existing_weeks.append({
                'week_start': week_start.strftime('%d.%m'),
                'week_end': (week_start + timedelta(days=4)).strftime('%d.%m'),
                'days': days
            })
        except WeeklyBreakfasts.DoesNotExist:
            pass

    if existing_weeks:
        return JsonResponse({
            'found': True,
            'pupil_name': f'{first_name} {last_name}',
            'weeks': existing_weeks
        })

    return JsonResponse({'found': False})


def pooling(request: HttpRequest):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            class_id = request.POST.get('class_name')

            pupil, created = Pupil.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                class_group_id=class_id
            )

            for key, value in request.POST.items():
                if key.startswith('breakfast_'):
                    date_str = key.replace('breakfast_', '')
                    breakfast_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    week_start_date = breakfast_date - timedelta(days=breakfast_date.weekday())

                    weekly_breakfast, _ = WeeklyBreakfasts.objects.get_or_create(
                        pupil=pupil,
                        week_start_date=week_start_date
                    )

                    weekday = breakfast_date.weekday()
                    day_attr = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'][weekday]

                    if value and value != 'none':
                        dish = Dish.objects.get(id=value)
                        setattr(weekly_breakfast, day_attr, dish)
                    else:
                        setattr(weekly_breakfast, day_attr, None)

                    weekly_breakfast.save()

            messages.success(request, f'Выбор для {first_name} {last_name} сохранён!')
            return redirect('/pool/')

        except Exception as e:
            messages.error(request, f'Ошибка при сохранении: {str(e)}')
            return redirect('/pool/')

    # GET
    classes = Class.objects.all().order_by('name')
    today = date.today()
    current_weekday = today.weekday()

    if current_weekday >= 4:
        days_until_monday = (7 - current_weekday) % 7
        first_week_start = today + timedelta(days=days_until_monday)
    else:
        first_week_start = today - timedelta(days=current_weekday)

    week_dates = []
    for week_offset in range(2):
        week_start = first_week_start + timedelta(days=week_offset * 7)
        for day_offset in range(5):
            day_date = week_start + timedelta(days=day_offset)
            if day_date >= today:
                week_dates.append(day_date)

    weeks_data = []
    current_week_dates = []
    current_week_data = []
    current_week_start = None

    for breakfast_date in week_dates:
        week_start = breakfast_date - timedelta(days=breakfast_date.weekday())
        if current_week_start != week_start:
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

        try:
            menu = DailyMenu.objects.get(date=breakfast_date)
            current_week_data.append({'date': breakfast_date, 'menu': menu, 'has_menu': True})
        except DailyMenu.DoesNotExist:
            current_week_data.append({'date': breakfast_date, 'menu': None, 'has_menu': False})

        current_week_dates.append(breakfast_date)

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
        'week_dates': week_dates,
    }
    return render(request, 'pool.html', context)


def index(request: HttpRequest):
    return render(request, 'index.html')