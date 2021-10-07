cd prodavnicesajt

export UKS_TEST_DB=ON
# collect static files and put inside ./static/
python3 manage.py collectstatic --noinput
# setup db
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py popuni_bazu
# run Django server
python3 manage.py runserver 0.0.0.0:8000
