================================
Diablo III Web Api Python Client
================================

.. image:: https://secure.travis-ci.org/sammyrulez/diablo-api-py.png?branch=master

Introduction
============
This is a Python module to query Diablo 3 public data (see https://github.com/Blizzard/d3-api-docs).
The Diablo 3 API resources are not publicly available: this implementation is based on the actual doc.


Installation
============

::

    pip install git+https://github.com/sammyrulez/diablo-api-py.git

Usage
=====

::

    #import module
    import diablo
    #instantiate a client for a specific host and player
    c = diablo.Client('host', 'battletag_name', 'battletag_number')
    #read career data
    career = c.career_profile()

The career object has the same structure as the json returned from the same api call https://github.com/Blizzard/d3-api-docs#career-profile-example.

Attributes name differs from the json fields: '-' has been replaced with '_' to match python syntax.

'heros' and 'last_hero_played' attributes have 'Lazy' object in which details are loaded from the remote service only if you invoke them
