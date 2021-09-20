<h1>Сервис по загрузке изображений на сервер</h1>

# API методы для взаимодействия с сервисом
1. GET Получение списка доступных изображений: http://localhost:8000/api/images/
2. GET Получение детальной информации о изображении: http://localhost:8000/api/images/id/
3. POST Загрузка одного изображения: http://localhost:8000/api/images/
4. DELETE Удаление: http://localhost:8000/api/images/id/
5. GET Изменение размеров изображения: http://localhost:8000/api/images/id/resize/
   * передача параметров осуествляется в url 
   * http://localhost:8000/api/images/id/resize/?width=500&height=500
6. GET Изменение поворота изображения: http://localhost:8000/api/images/rotate/
   * передача параметров осуествляется в url 
   * http://localhost:8000/api/images/id/resize/?degree=270
7. GET Изменение формата изображения (с jpeg на png и наоборот): http://localhost:8000/api/images/conver/
8. GET Применение сразу и размера и поворота изображения: http://localhost:8000/api/images/all/
   * передача параметров осуествляется в url 
   * http://localhost:8000/api/images/id/resize/?width=500&height=500&degree=270

   
# Настройка проекта
1. pip install -r requirements.txt 
2. python manage.py makemigrations 
3. python manage.py migrate 
4. python manage.py runserver

Все команды запускаются из главной директории с проектом