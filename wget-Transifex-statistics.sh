#!/bin/bash
#
# We want to serve the transifex language statistics image on our server,
# as opposed to cloudfront, google, whathaveyou. People should not have 
# to blindly load images from around the net. We can serve a copy!
#
# There should be a cronjob running on the production system
# running this script once per hour or daily or so...
#
# keep the old version and give it a filename containing a date stamp 
mv c3sintent/static/C3Sintent-transifex-languages.png  c3sintent/static/C3Sintent-transifex-languages-`date "+%Y-%m-%d-%H%M"`.png
# get a more recent version
wget https://www.transifex.com/projects/p/C3Sintent/resource/POT/chart/image_png -O c3sintent/static/C3Sintent-transifex-languages.png
#
# done!
