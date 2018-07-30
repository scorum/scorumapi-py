from distutils.core import setup

setup(
    name='scorumapi',
    version='0.0.1',
    packages=['api', 'utils'],

    entry_points={
        'console_scripts': [
            'accounts_to_csv = utils.accounts_to_csv:main',
            'posts_to_csv = utils.posts_to_csv:main',
            'scorumapi = utils.scorumapi:main'
          ]
      },
)