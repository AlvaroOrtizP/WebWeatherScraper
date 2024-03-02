from setuptools import setup, find_packages

setup(
    name='proyecto_python',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'main.py = src.main:main',
            'WindWuLogger.py = src.WindWuLogger:main',
            'TemperaturaLogger.py = src.TemperaturaLogger:main',
            'TomarCapturaWindWuru.py = src.TomarCapturaWindWuru:main'
        ],
    },
    install_requires=[
        'requests',
        'selenium'
    ],
)
