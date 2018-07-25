from setuptools import setup

if __name__ == "__main__":
    setup(
        name='airwaves',
        version='0.0.2',
        url='https://github.com/umd_mith/airwaves',
        author='Ed Summers',
        author_email='ehs@pobox.com',
        packages=['airwaves', ],
        description='Unlocking the Airwaves Utilities',
        python_requires='>=2.7',
        install_requires=['requests'],
        entry_points={'console_scripts': ['airwaves = airwaves:main']}
    )
