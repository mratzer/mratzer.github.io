#!/bin/bash

ARTIST=marrat.eu

TILE_WIDTH=400
TILE_HEIGHT=630

CURRENT_WIDTH=0
CURRENT_OFFSET=0

INPUT_DIRECTORY="$1"
RESULT_FILE=_site/assets/preview.jpg

rm -f $RESULT_FILE

for INPUT in $INPUT_DIRECTORY/DSCF*.jpg; do
	((CURRENT_WIDTH+=TILE_WIDTH))
	
	if [ -z ${foo+x} ]; then
		cp $INPUT $RESULT_FILE
		foo=notempty
	else
		jpegtran -perfect -crop "$CURRENT_WIDTH"x"$TILE_HEIGHT"+0+0 -outfile $RESULT_FILE $RESULT_FILE
		jpegtran -perfect -drop +"$CURRENT_OFFSET"+0 $INPUT -outfile $RESULT_FILE $RESULT_FILE
	fi

	((CURRENT_OFFSET+=TILE_WIDTH))
done

jpegtran -perfect -copy none -progressive -optimize -outfile $RESULT_FILE $RESULT_FILE
exiftool -q -overwrite_original -all= -tagsFromFile @ -artist=$ARTIST -copyright=$ARTIST $RESULT_FILE
