dj
========

`dj` is a small command line utility for estimating the key and bpm of an audio file.

## Installation

```
git clone https://github.com/abelsonlive/dj.git
cd dj/
sudo python setup.py install
```

**NOTE**: `dj` relies on [Essentia's](https://github.com/MTG/essentia/) audio-analysis executable, [`essentia_streaming_extractor_freesound`](https://github.com/MTG/essentia/blob/master/doc/sphinxdoc/extractors_out_of_box.rst). The [provided version](dj/essentia_streaming_extractor_freesound) should work out-of-the-box on Mac OSX, but if not, [install Essentia](http://essentia.upf.edu/documentation/installing.html) on your machine and replace the provided version by with one generated by the Essentia build.


## Usage

```
$ dj <file>
>>> {"bpm": 125.0, "key": "Fm"}
```

