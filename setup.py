from setuptools import setup

setup(
    name='pskill',
    version='0.1',
    packages=[''],
    url='https://github.com/jubnzv/pskill',
    license='MIT',
    author='Georgy Komarov',
    author_email='jubnvz@gmail.com',
    description='Simple cli util to kill process by it port.', install_requires=['tabulate', 'psutil', 'docopt']
)
