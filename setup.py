import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pyramid',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'velruse',
    'alembic',
    'deform',
    'colander',
    'Babel'
    ]

setup(name='turnsapi',
      version='0.0',
      description='turnsapi',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='turnsapi',
      install_requires=requires,
      message_extractors = { 'turnsapi': [
          ('**.py', 'python', None),
          ('templates/**.html', 'mako', None),
          ('templates/**.mako', 'mako', None),
          ('templates/**.mak', 'mako', None),
          ('static/**', 'ignore', None)]},
      entry_points="""\
      [paste.app_factory]
      main = turnsapi:main
      [console_scripts]
      initialize_turnsapi_db = turnsapi.scripts.initializedb:main
      """,
      )
