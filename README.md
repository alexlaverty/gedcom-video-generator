# gedcom-video-generator

Generate a Familiy History video from a GEDCOM file

The purpose of this project is to attempt to read a GEDCOM file and generate an 
interesting multimedia rich family tree geneaology history video that you can share with your friends and family.

The script will start with a specified person and then recursively walk up the tree through the paternal ancestors, reading out information about each person along the way.

The project is written in python and the main libraries used are :

* [python-gedcom](https://github.com/nickreynke/python-gedcom)
* [MoviePy](https://zulko.github.io/moviepy/)
* [Amazon Polly Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

To get started, mv the config-example.py to config.py and fill in the api keys to access AWS Amazon Polly for the speech to text translation.

In app.py specify the Invidiual ID that you want to start with :

```
starting_id = "@I0000@"
```

then run 

```
python app.py
```