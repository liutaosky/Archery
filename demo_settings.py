# -*- coding: UTF-8 -*-
# 临时演示配置，用于快速查看资源管理模块效果

from archery.settings import *

# 使用 SQLite 数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'archery.db'),
    }
}

# 简化缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'dingding': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Django-Q 同步模式
Q_CLUSTER = {
    'name': 'archery',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'cpu_affinity': 1,
    'save_limit': 0,
    'queue_limit': 50,
    'label': 'Django Q',
    'django_redis': 'default',
    'sync': True
}

# 禁用 LDAP
ENABLE_LDAP = False

# 简化密码验证
AUTH_PASSWORD_VALIDATORS = []
