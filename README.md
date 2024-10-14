# bfr-track-trace

## Architecture

* `read_img.py` converts track to point file (in `points` folder). 
* `draw_spline.py` uses point file to approximate spline, and saves csv data to `spline_data` folder.
* Use `requirements.txt` to install dependencies. 
* Put input images in `images` folder.
* See result images in `results` folder.

## Instructions

**Run `python3 read_img.py -f <FILENAME>`, then run `python3 draw_spline.py -f <FILENAME>`. Make sure input image is a PNG, and has been saved in `images` folder.**
* `--filename` or `-f` corresponds to input image file name. This field is **mandatory**. This file is assumed to be a PNG.
* *Example call: If the file name is `sample_image.png`, and our calls might be:*
    * `python3 read_img.py -f sample_image`
    * `python3 draw_spline.py -f sample_image`

**Optional Arguments For `draw_spline.py`**
* `--smoothing` corresponds to smoothing factor for spline approximation in `draw_spline.py`. Default is 500 (but can go down to ~100 for more granularity on larger track).
* `--close_loop` will manually ensure a closed track in `draw_spline.py`. Default is False; this should only be used for the larger track where there exists a closed track to be drawn. 

## Results
![results_one](results/1_spline.png)
![results_two](results/2_spline.png)

### End Notes

Made October 2024 by Eva Schiller (with help from GenAI).
Contact me (Eva) with questions!

