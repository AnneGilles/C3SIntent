help us translate this app to more languages
============================================

please go to the relevant project on transifex and translate away :-)

  https://www.transifex.com/projects/p/C3Sintent/


procedure of managing translations
==================================

once you edit code and or templates and there are new strings to be translated,
follow these steps to get the new translations ready and working:

  python setup.py extract_messages

will search code and templates and update the PO template (POT). To use transifex
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
