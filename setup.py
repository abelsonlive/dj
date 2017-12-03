from setuptools import setup

def build():
  setup(
    name = "dj",
    version = "0.0.1",
    author = "Brian Abelson",
    author_email = "brianabelson@gmail.com",
    description = "Extract bpm + key from an audio file.",
    license = "MIT",
    keywords = "dj",
    url = "https://github.com/abelsonlive/dj",
    packages = ['dj'],
    install_requires = [],
    package_data={
        'dj': ['essentia_streaming_extractor_freesound'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Communications :: Email",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
    'console_scripts': [
        'dj = dj:main'
        ]
    }
  )

if __name__ == '__main__':
  build()