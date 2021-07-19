# create venv

`virtualenv venv`

# activate venv

`source venv/bin/activate`

# install locally

`pip install -r requirements.txt`

# deactivate venv

`deactivate`

# Execute

Need to pass three parameters in sequence

- 1st language for English 'En' for German 'De'
- 2nd 'text' or 'url' (the python code can give the accuracy result for a webpage or a text)
- 3rd pass full URL or pass text file path

For Example

- To get result of a web page which is in english
  `python main.py en url https://www.vnrag.de/about-vnr/`
- To get result of a text which is in english
  `python main.py en text sample.txt`
  (sample.txt file contains the text needs to be scored)

The Code gives result as a grade as in who can read the text and also gives additional details to know more about the text
Refrence Grade Table
||||
|--- |--- |--- |
|Score|Age|Grade Level|
|1|5-6|Kindergarten|
|2|6-7|First/Second Grade|
|3|7-9|Third Grade|
|4|9-10|Fourth Grade|
|5|10-11|Fifth Grade|
|6|11-12|Sixth Grade|
|7|12-13|Seventh Grade|
|8|13-14|Eighth Grade|
|9|14-15|Ninth Grade|
|10|15-16|Tenth Grade|
|11|16-17|Eleventh Grade|
|12|17-18|Twelfth grade|
|13|18-24|College student|
|14|24+|Professor|
