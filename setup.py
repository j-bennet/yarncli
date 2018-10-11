from setuptools import setup, find_packages

install_requirements = [
    'yarn-api-client==0.2.3',
    'prompt-toolkit>=2.0.0'
]

dependency_links = [
    'https://github.com/jonathanslenders/python-prompt-toolkit/tarball/2.0#egg=prompt_toolkit-2.0.0'
]

setup(
    name='yarncli',
    author='Irina Truong',
    author_email='irinatruong@gmail.com',
    version='0.0.1',
    license='BSD',
    url='http://yarncli.com',
    packages=find_packages(),
    description='CLI for YARN cluster.',
    long_description=open('README.md').read(),
    install_requires=install_requirements,
    dependency_links=dependency_links,
    entry_points='''
        [console_scripts]
        yarncli=yarncli.main:cli
    ''',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System',
        'Topic :: System :: Monitoring',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
