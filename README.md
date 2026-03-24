Repository for my static homepage.

---


# Usage
## Prerequisites
1. `jpegtran` - used for lossless modififcation of the JPG file
2. `exiftool` - used to remove sensitive EXIF data from the JPG file
3. Python 3
## Build site
1. Create JPG files with _max._ dimensions of **1000** x **1000** pixels with the name **DSCF*.jpg** (e.g., _DSCF0001.jpg_) somewhere.
2. Prepare images and metadata: `./prepare_photos.py ../path/to/that/directory`
	1. To start counting with another number (e.g., `13`), use `./prepare_photos.py ../path/to/photo/directory 13`
3. Modify the newly generated `photos.yaml` if needed (e.g., `additional_gear` or missing lens information for manual ones). The backup of the previous file `photos.yaml.bak` might come in handy.
4. Generate HTML: `./render_site.py`
## Generate Link Preview Image
1. Create **three** JPG files with _exact_ dimensions of **400** x **630** pixels with the name **DSCF*.jpg** (e.g., _DSCF0001.jpg_) somewhere.
2. Generate preview image: `./prepare_preview.sh ../path/to/that/directory`
## Misc
1. Run locally: `./run_locally.sh`


---

# TODOs

3. Remove deleted photos from repository.
4. Galleries (?)

