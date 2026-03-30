#!/usr/bin/env bash

pip install -r requirements.txt

cd metanit

python manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.get_or_create(username='admin',
defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}); user = User.objects.get(username='admin');
user.set_password('password'); user.save()" | python manage.py shell

python manage.py collectstatic --noinput
