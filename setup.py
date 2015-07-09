from setuptools import setup

setup(name='graphql',
      version='0.1',
      description='graphql parser',
      url='https://github.com/AdrielVelazquez/graphql',
      author='Adriel Velazquez',
      author_email='adriel@set.tv',
      test_suite='nose.collector',
      tests_require=['nose'],
      license='MIT',
      packages=['graphql'],
      zip_safe=False)