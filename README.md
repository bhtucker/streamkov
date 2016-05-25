# streamkov

Stream text into a Markov chain and draw sequences out while processing.

![Frontend example](http://i.imgur.com/erHoYh7.png)

# Features

* Provide a url to a twitter account or text file to build new markov chains
* Draw sentences from the current chain with generate button
* Even while this new data is being read in, you'll be able to draw sentences from the chain so far!
* You can also combine chains by checking their boxes and hitting 'blend'

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

