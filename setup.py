"""
Extract some statistics from Trello JSON dump
"""
from setuptools import setup

setup(
    name='strello',
    version='0.1.0.dev',
    url='https://github.com/noirbizarre/strello',
    license='MIT',
    author='Axel Haustant',
    author_email='noirbizarre@gmail.com',
    description='Extract some statistics from Trello JSON dump',
    long_description=__doc__,
    py_modules=['strello'],
    zip_safe=False,
    platforms='any',
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'strello = strello:cli',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
