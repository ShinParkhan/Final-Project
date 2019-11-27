from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY', default='&&@a!_y0##=v!@evd=olh@^n6(6i$(z!ue59$r^w30zxdrr(f$')

DEBUG = True

ALLOWED_HOSTS = []