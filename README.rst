===============================================================================
README
===============================================================================

Plone product which makes files from the file system available within plone.

    - http://pypi.python.org/pypi/fui.memberlist/
    - http://github.com/espenak/fui.memberlist/


Install
-------

You can install this product in Plone using buildout.

    1. Add ``fui.memberlist`` to ``buildout.cfg``::

        [buildout]
        ...
        eggs =
            ...
            fui.memberlist

        [instance]
        ...
        zcml = 
            ...
            fui.memberlist

    2. Run (maybe backup first..)::

        ~$ buildout -N

    3. Install the plugin using *Site Setup* in your Plone site.




For developers
--------------

Release a new version to pypi.python.org with::

    ~$ python setup.py egg_info -RDb "" sdist upload
