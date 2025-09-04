from setuptools import setup, find_packages
import os

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ytclip',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A fast YouTube video clip downloader with timestamp support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ytclip',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Video',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'yt-dlp>=2024.1.0',
    ],
    entry_points={
        'console_scripts': [
            'ytclip=ytclip.cli:main',
        ],
    },
    keywords='youtube video downloader clip timestamp ffmpeg',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/ytclip/issues',
        'Source': 'https://github.com/yourusername/ytclip',
    },
)