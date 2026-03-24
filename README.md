Repository for my static homepage.

---


# Usage
## Prerequisites
1. `jpegtran` - used for lossless modifications of JPG files
2. `exiftool` - used to remove sensitive EXIF data from JPG files
3. Python 3
## Build Site
1. Create JPG files with _max._ dimensions of **1000** x **1000** pixels with the name **DSCF*.jpg** (e.g., _DSCF0001.jpg_) somewhere.
2. Prepare images and metadata: `./scripts/prepare_photos.py ../path/to/that/directory`
3. Modify the newly generated `photos.yaml` if needed (e.g., `additional_gear` or missing lens information for manual ones). The generated backup of the previous file `photos.yaml.bak` might come in handy.
4. Generate HTML: `./scripts/render_site.py`
## Generate Link Preview Image
1. Create **three** JPG files with _exact_ dimensions of **400** x **630** pixels with the name **DSCF*.jpg** (e.g., _DSCF0001.jpg_) somewhere.
2. Generate preview image: `./prepare_preview.sh ../path/to/that/directory`
## Remove Unused Photos
1. Remove all unused photos: `./scripts/clear_photos.py`
	1. Unused photos are identified by their existence in `./_site/assets/*.jpg` compared to entries in the `photos.yaml` file (so, _after_ running `./scripts/prepare_photos.py`).

## Misc
1. Run locally: `./scripts/run_locally.sh`
2. Run everything in one go: `./go.sh ../path/to/photos ../path/to/preview-photos`
	1. The 2nd directory (preview photos) is optional


---

# TODOs

4. Galleries (?)
