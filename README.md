# bfr-track-trace

## Architecture

* `read_img.py` converts track to point file (in `points` folder). 
* `draw_spline.py` uses point file to approximate spline, and saves csv data to `spline_data` folder.
* Use `requirements.txt` to install dependencies. 
* Put input images in `images` folder.
* See result images in `results` folder.

## Instructions

* `FILENAME` corresponds to input image file name in **both** `read_img.py` an `draw_spline.py`.
* `SMOOTHING` corresponds to smoothing factor for spline approximation in `draw_spline.py`, best around 400 to 500 (but can go down to ~100 for more granularity on larger track)
* `CLOSE_LOOP` will manually ensure a closed track in `draw_spline.py`, should only be used for the larger track where there exists a closed track to be drawn. 

## Results
![results_one](results/1_spline.png)
![results_two](results/2_spline.png)

### End Notes

Made October 2024 by Eva Schiller.
Contact me (Eva) with questions!

