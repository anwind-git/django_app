from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('./logs/info.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def index(request):
    logger.info('Просмотр страницы, главная')
    return render(request, 'myapp/index.html', {'title': 'Главная страница'})


def about(request):
    logger.info('Просмотр страницы, информация о сайте'),
    return render(request, 'myapp/about.html', {'title': 'Информация о сайте'})
