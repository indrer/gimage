# Gimage - GitHub as an image hosting service

This is a simple Python script as a proof of concept inspired by [this post](https://news.ycombinator.com/item?id=31631144).

## Flags

- `-nr` - creates new repository
- `--repo` - the name of the repo where your images will be uploaded (make the name as short as possible!)
- `--add_token` - your public access token

## How to run

Before you begin, make sure you have Python 3.x installed.

1. Install pip.
2. Run `pip install -r requirements`
3. Create a GitHub account.
4. [Create a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) (PAT) and select _public_repo_ as the access scope.
5. Clone this repo.
6. The first time you run the script, you have to provide the name of your public repo and your PAT. The script can create a repo for you if you add `-nr` flag. A file will be created storing your PAT and the repo name, so you will not need to provide them later on.

An example of the first time script run:
``` 
python .\main.py --add_token xxx_xxx --repo img -nr C:\Users\indrer\image.png
```

When the settings file is generated, you can simply run the script as:
```
python .\main.py C:\Users\indrer\image.png
```

The script copies the image url to your clipboard.