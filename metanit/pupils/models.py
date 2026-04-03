from django.db import models
from django.utils.translation import gettext_lazy as _


class Class(models.Model):
    name = models.CharField(max_length=10, verbose_name='Название класса')
    number_of_pupils = models.IntegerField(verbose_name='Количество учеников')

    class Meta:
        verbose_name = _('Класс')
        verbose_name_plural = _('Классы')

    def __str__(self):
        return f"{self.name}"


class Pupil(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')

    class Meta:
        verbose_name = _('Ученик')
        verbose_name_plural = _('Ученики')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Dish(models.Model):
    short_name = models.CharField(max_length=100, verbose_name='Короткое название блюда')
    name = models.CharField(max_length=200, verbose_name='Название блюда', default='')

    class Meta:
        verbose_name = _('Завтрак')
        verbose_name_plural = _('Завтраки')

    def __str__(self):
        return self.short_name


class DailyMenu(models.Model):
    date = models.DateField(verbose_name='Дата')
    option_1 = models.ForeignKey(Dish, on_delete=models.CASCADE,
                                 related_name='menu_option_1', verbose_name='Вариант завтрака 1')
    option_2 = models.ForeignKey(Dish, on_delete=models.CASCADE,
                                 related_name='menu_option_2', verbose_name='Вариант завтрака 2')

    class Meta:
        verbose_name = _('Ежедневное меню')
        verbose_name_plural = _('Ежедневное меню')
        unique_together = ['date']

    def __str__(self):
        return f"Меню на {self.date}"


class WeeklyBreakfasts(models.Model):
    pupil = models.OneToOneField(Pupil, on_delete=models.CASCADE, verbose_name="Ученик")

    monday = models.ForeignKey(Dish, on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name="Понедельник",
                               related_name="monday_breakfasts")
    tuesday = models.ForeignKey(Dish, on_delete=models.SET_NULL,
                                null=True, blank=True, verbose_name="Вторник",
                                related_name="tuesday_breakfasts")
    wednesday = models.ForeignKey(Dish, on_delete=models.SET_NULL,
                                  null=True, blank=True, verbose_name="Среда",
                                  related_name="wednesday_breakfasts")
    thursday = models.ForeignKey(Dish, on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name="Четверг",
                                 related_name="thursday_breakfasts")
    friday = models.ForeignKey(Dish, on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name="Пятница",
                               related_name="friday_breakfasts")

    week_start_date = models.DateField(verbose_name='Дата начала недели')

    class Meta:
        verbose_name = _('Выбор завтрака на неделю')
        verbose_name_plural = _('Все выборы завтрака на неделю')

    def __str__(self):
        return f"{self.pupil}"
