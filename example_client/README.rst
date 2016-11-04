=============================
Fee Calculator Example Client
=============================

An example client using the fee calculator built in ES6 using the `Redux <http://redux.js.org/>`__ framework with `Reactjs <https://facebook.github.io/react/>`__.


Dependencies
============
-  `nodejs <http://nodejs.org/>`__ (v6.2.0 - can be installed using `nvm <https://github.com/creationix/nvm>`_)


Installation
============

Install dependencies:

::

    npm install


Develop
=======

Run against local dev fee calculator api on `http://localhost:8000/api/v1`

::

    npm start

Or against any arbitray fee calculator

::

    REACT_APP_API_URL=http://example.com/api/v1 npm start


Prod
====

Build

::

    REACT_APP_API_URL=http://example.com/api/v1 npm run build

This will result in a directory `build`

Serve

::

    npm run serve
