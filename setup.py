from setuptools import setup

setup(
    name='stptimer',
    version='0.1',
    description='The coolest standup timer CLI',
    url='https://github.com/fizzy-drinks/stptimer',
    author='fizzy',
    license='MIT',
    packages=['stptimer'],
    zip_safe=True,
    entry_points={
        'console_scripts': ['stptimer=stptimer.timer:main']
    }
)
