 ______     ______     ______     ______     ______   ______   ______    
/\  ___\   /\  __ \   /\___  \   /\  ___\   /\__  _\ /\__  _\ /\  ___\   
\ \ \__ \  \ \  __ \  \/_/  /__  \ \  __\   \/_/\ \/ \/_/\ \/ \ \  __\   
 \ \_____\  \ \_\ \_\   /\_____\  \ \_____\    \ \_\    \ \_\  \ \_____\ 
  \/_____/   \/_/\/_/   \/_____/   \/_____/     \/_/     \/_/   \/_____/ 
                                                                         


# GAZETTE

***WARNING**: This is a project in in **ALPHA**. You should expect to encounter many broken things and backwards comparability should not be expected. Please break it!*

Gazette is a static site generator. There are no plugins or themes.

## Demo

*  [Mr. Rigden's Blog](https://slides.rigden.dev)
*  [Seattle Podcasters Guild](https://seattlepodcasters.com)

## Installation

Gazette requires Python 3. If you are still using Python 2, stop. Clone the repo, enter the directory, make a python virtual enviroment, and install the requirements.

    git clone https://github.com/mr-rigden/gazette.git
    cd gazette
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Usage

### Help
Get help with the `-h` argument:

    python gazette.py -h
    
You'll get something like this as the result

    usage: gazette.py [-h] [-v] [-i] path
    
    A static site generator for blogs and podcasts. v0.1.1
    
    positional arguments:
      path              path to site
    
    optional arguments:
      -h, --help        show this help message and exit
      -v, --verbose     increase verbosity
      -i, --initialize  initialize site

### Initialization

Initialize a new site with `-i` and point it at an empty directory. 

    python gazette.py -i ~/sites/demo.rigden.dev

This create several files and directories. 
* config.yaml - This contain your site specific settings
* content -  This directory will contain the files used to generate pages
* favicon.ico - A default favicon.ico.
* footer.html - The contents of this file will be added to all pages just above the closing body tag.
* header.html - The contents of this file will be added to all pages just above the closing head tag.
* output - This directory will contain the finished html files.
* post_ending.html - The contents of this file will be added the ending of all posts.

### Rendering

Pointing gazette at an initialized directory with no arguements with render the site.

    python gazette.py ~/sites/demo.rigden.dev

## History
* August 29, 2019 - Initial testing release v0.1.1 

## Authors

[Jason Rigden](https://twitter.com/mr_rigden)


## License
**MIT License**

Copyright (c) 2019 Jason Rigden

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

