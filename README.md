# streamkov

Stream text into a Markov chain and draw sequences out while processing.


# Features

* Supply URLs to textfiles via `/read/{url}` 
* Upload textfiles yourself via the form at index
* Draw sentences from the chain via `/draw/`
* Even if many files are being processed, you'll be able to draw from the current chain unimpeded.

# Running

Streamkov is intended for Python 3.5.

To clone and run locally, simply:

`pip install .`

from main directory, then

`python streamkov/app.py`

