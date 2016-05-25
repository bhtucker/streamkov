# streamkov

Stream text into a Markov chain and draw sequences out while processing.

![Frontend example](http://i.imgur.com/erHoYh7.png)

# Features

* Supply URLs to textfiles via `/read/{url}` 
* Upload textfiles yourself via the form at index
* Draw sentences from the chain via `/draw/`
* Even if many files are being processed, you'll be able to draw from the current chain unimpeded.

# Installation

Streamkov is intended for Python 3.5. It uses PostgreSQL, by default looking for a database called `streamkov`

It expects to use your Twitter API key, so you'll need to create a `secrets.py` with the required credentials.

To run locally, simply `clone` and then:

`pip install .`

from main project directory, then from the `frontend` directory, build the JS app via:

`npm install`
and
`npm run build`

to create the `dist` directory with static assets and all of the required JS in `bundle.js`.

# Running
Finally, run the app!

`python streamkov/app.py`

