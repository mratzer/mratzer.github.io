#!/bin/bash

PHOTOS_DIRECTORY="$1"
PREVIEW_DIRECTORY="$2"

if [ -z "$PHOTOS_DIRECTORY" ]; then
  echo "Usage: $0 <photos_directory> [<preview_directory>]"
  exit 1
fi

if [ ! -d "$PHOTOS_DIRECTORY" ]; then
  echo "Error: '$PHOTOS_DIRECTORY' is not a valid directory"
  echo "Usage: $0 <photos_directory> [<preview_directory>]"
  exit 1
fi

if [ -n "$PREVIEW_DIRECTORY" ] && [ ! -d "$PREVIEW_DIRECTORY" ]; then
  echo "Error: '$PREVIEW_DIRECTORY' is not a valid directory"
  echo "Usage: $0 <photos_directory> [<preview_directory>]"
  exit 1
fi


./scripts/prepare_photos.py $PHOTOS_DIRECTORY \
&& if [ -n "$PREVIEW_DIRECTORY" ]; then
  ./scripts/prepare_preview.sh $PREVIEW_DIRECTORY
fi \
&& ./scripts/render_site.py \
&& ./scripts/clear_photos.py \
&& ./scripts/run_locally.sh
