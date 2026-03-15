Repository for my static homepage.

---

# Usage

1. Prerequisites:
	1. `jpegtran` - used for lossless modififcation of the JPG file
	1. `exiftool` - used to remove sensitive EXIF data from the JPG file
	1. Python 3
1. Prepare images and metadata: `./prepare_photos.py ../path/to/photo/directory`
	1. To start counting with another number (e.g., `13`), use `./prepare_photos.py ../path/to/photo/directory 13`

1. Modify the newly generated `photos.yaml` if needed (e.g., `additional_gear` or missing lens information for manual ones)
1. Generate HTML: `./render_site.py`
1. Run locally: `./run_locally.sh`

---

# TODOs

1. Read metadata file if present and derive counter from there. Also, avoid having to handle manual information every time.
1. Add new photos between existing ones.
1. Remove photos.
1. Galleries (?)

