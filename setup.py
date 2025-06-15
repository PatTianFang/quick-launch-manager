from setuptools import setup, find_packages

setup(
    name='quick-launch-manager',
    version='0.1.0',
    author='Fang Tian',
    author_email='PatTianFang@outlook.com',
    description='A tool to manage shortcuts on Windows and display them in the taskbar.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            'quick-launch-manager=main:main',  # Adjust according to your main function
        ],
    },
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)