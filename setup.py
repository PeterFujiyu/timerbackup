import platform
from setuptools import setup

# 根据操作系统选择所需的模块
required_modules = ['watchdog', 'tkinter', 'pycryptodomex']
if platform.system() == 'Linux':
    required_modules.append('python-crontab')

setup(
    name='incremental-backup',
    version='1.0.0',
    description='Incremental Backup Script',
    author='Peter',
    author_email='jiyu.fu@outlook.com',
    packages=[''],
    install_requires=required_modules,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux' if platform.system() == 'Linux' else 'Operating System :: Microsoft :: Windows',
    ],
)
