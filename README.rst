================================
Diablo III Web Api Python Client
================================

Installation
============

pip install pip install git+https://github.com/sammyrulez/diablo-api-py.git

Usage
=====

    import diablo
	c = diablo.Client('host', 'battletag_name', 'battletag_number')
	career = c.career_profile()
