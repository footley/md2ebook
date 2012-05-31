md2ebook.py
===========

Converts a simple markdown document into the main ebook formats (epub, mobi\prc, html and pdf).

Installation
------------

```
pip install git+git://github.com/footley/md2ebook.git#egg=md2ebook
```

Assumptions
-----------

* The title of the book is the first h1 element.
* Each Chapter starts with an h2 element.
* The authors name is the first h3
* If only one Chapter is present no Table of Contents is generated.

Therefore valid markdown must contain at least one h1, h2 and h3.

Simple Example (note the newlines between paragraphs)
--------------

```md
Treasure Island
===============
    
### Robert Louis Stevenson
    
The Old Sea-dog at the Admiral Benbow
-------------------------------------
    
Squire Trelawney, Dr. Livesey, and the rest of these gentlemen having asked me to write down the whole particulars about Treasure Island, from the beginning to the end, keeping nothing back but the bearings of the island, and that only because there is still treasure not yet lifted, I take up my pen in the year of grace 17-, and go back to the time when my father kept the Admiral Benbow inn and the brown old seaman with the sabre cut first took up his lodging under our roof. I remember him as if it were yesterday, as he came plodding to the inn door, his sea-chest following behind him in a hand-barrow-a tall, strong, heavy, nut-brown man, his tarry pigtail falling over the shoulder of his soiled blue coat, his hands ragged and scarred, with black, broken nails, and the sabre cut across one cheek, a dirty, livid white. I remember him looking round the cover and whistling to himself as he did so, and then breaking out in that old sea-song that he sang so often afterwards:

"Fifteen men on the dead man's chest-

Yo-ho-ho, and a bottle of rum!"

in the high, old tottering voice that seemed to have been tuned and broken at the capstan bars. Then he rapped on the door with a bit of stick like a handspike that he carried, and when my father appeared, called roughly for a glass of rum. This, when it was brought to him, he drank slowly, like a connoisseur, lingering on the taste and still looking about him at the cliffs and up at our signboard.
"This is a handy cove," says he at length; "and a pleasant sittyated grog-shop. Much company, mate?" My father told him no, very little company, the more was the pity.
    
Black Dog Appears and Disappears
--------------------------------
    
It was not very long after this that there occurred the first of the mysterious events that rid us at last of the captain, though not, as you will see, of his affairs. It was a bitter cold winter, with long, hard frosts and heavy gales; and it was plain from the first that my poor father was little likely to see the spring. He sank daily, and my mother and I had all the inn upon our hands, and were kept busy enough without paying much regard to our unpleasant guest.

It was one January morning, very early-a pinching, frosty morning-the cove all grey with hoar-frost, the ripple lapping softly on the stones, the sun still low and only touching the hilltops and shining far to seaward. The captain had risen earlier than usual and set out down the beach, his cutlass swinging under the broad skirts of the old blue coat, his brass telescope under his arm, his hat tilted back upon his head. I remember his breath hanging like smoke in his wake as he strode off, and the last sound I heard of him as he turned the big rock was a loud snort of indignation, as though his mind was still running upon Dr. Livesey.
```

Command Line Usage
------------------

```
usage: md2ebook.py [-h] [--covers [COVERS [COVERS ...]]] [--output OUTPUT]
                   [-html] [-pdf] [-epub] [-mobi] [-prc]
                   files [files ...]

Convert provided markdown to html, pdf, epub and mobi

positional arguments:
  files                 list the markdown files to be converted

optional arguments:
  -h, --help            show this help message and exit
  --covers [COVERS [COVERS ...]], -c [COVERS [COVERS ...]]
                        provide the paths for the covers to be used
  --output OUTPUT, -o OUTPUT
                        output directory, if different from input files
                        directory
  -html                 suppress convertion to html
  -pdf                  suppress convertion to pdf
  -epub                 suppress convertion to epub
  -mobi                 suppress convertion to mobi
  -prc                  suppress convertion to prc
```

