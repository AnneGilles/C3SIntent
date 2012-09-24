help us translate this app to more languages
============================================

please go to the relevant project on transifex and translate away :-)

  https://www.transifex.com/projects/p/C3Sintent/


procedure of managing translations
==================================

once you edit code and or templates and there are new strings to be translated,
follow these steps to get the new translations ready and working:

  python setup.py extract_messages

will search code and templates and update the PO template (POT).


Some notes about lingua, especially lingua_xml
==============================================
The extraction process uses lingua_python for python files (.pt) and lingua_xml
for chameleon templates (.pt) as can be seen in setup.py. Please make sure to
use valid XML syntax in your templates, because otherwise lingua_xml will just
skip the remainder and not produce all the relevant output.


Using transifex.com
===================
To use transifex
as a hub for translations to ease engagement of translators (usually non-developers),
you as the developer can integrate this in your app by using the transifex client.
It works similar to git in terms of pushing and pulling translations:

  pip install transifex-client

For the following, you need an account on transifex.com and of course the necessary
rights to manage the project.

  tx push -s

will upload the source POT to transifex.com, where you (and others) may work
on those translations and add new strings.

  tx pull

will download the relevant .po files

  python setup.py compile_catalog

will then compile the .po files to .mo files usable by the apps translation machinery.


Advanced: i18n for developers
=============================

What if your message extraction yields <dynamic element> tags in the PO files?
Check out Wicherts answer to a "feature request":

  https://github.com/wichert/lingua/issues/12

Something to study from the plonistas:

  http://plone.org/documentation/kb/i18n-for-developers
