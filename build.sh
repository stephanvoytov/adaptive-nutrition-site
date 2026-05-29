#!/usr/bin/env bash

pip install -r requirements.txt

cd metanit

python manage.py migrate

echo "Creating superuser (set DJANGO_SUPERUSER_PASSWORD env var or default will be used)..."
if [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
  DJANGO_SUPERUSER_PASSWORD="admin123"
  echo "⚠ Using default password 'admin123'. Set DJANGO_SUPERUSER_PASSWORD env var for production."
fi
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.get_or_create(username='admin',
defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}); user = User.objects.get(username='admin');
user.set_password('$DJANGO_SUPERUSER_PASSWORD'); user.save()" | python manage.py shell

python manage.py collectstatic --noinput
