from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

if __name__ == "__main__":
    setup(
        name='airwaves',
        version='0.1.0',
        url='https://github.com/umd_mith/airwaves',
        author='Ed Summers',
        author_email='ehs@pobox.com',
        packages=['airwaves', ],
        description='Unlocking the Airwaves Utilities',
        long_description=long_description,
        long_description_content_type="text/markdown",
        python_requires='>=2.7',
        install_requires=['requests', 'click'],
        test_requires=['pytest'],
        setup_requires=['pytest-runner'],
        entry_points={'console_scripts': ['airwaves = airwaves.cli:cli']}
    )
