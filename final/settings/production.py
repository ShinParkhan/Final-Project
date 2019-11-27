from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['bonomovie.mtpppimcwz.ap-northeast-2.elasticbeanstalk.com']