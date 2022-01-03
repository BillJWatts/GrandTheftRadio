# Grand Theft Radio

Discord bot providing access to all radio channels accross all gta titles.
To run the bot you will need to get a discord api token and install some
dependencies. A `Dockerfile` has been provided for convenience.

## Creating A bot
To get an api token [this tutorial](https://www.writebots.com/discord-bot-token/)
does a pretty good job of explaining how to get one.

## Running with docker
This assumes the `DISCORD_API_TOKEN` is avalible as an environment variable.

To build the container:

### build
```
docker build . -t grand_theft_radio
```

Then to run it:

### run
```
docker run -d -e DISCORD_API_TOKEN=$DISCORD_API_TOKEN grand_theft_radio
```

## Local Dependencies:
You will need to install the following dependencies before running the code

### ubuntu
```
sudo apt-get install ffmpeg python-dev
```

### fedora
```
sudo dnf install ffmpeg python-devel
```

### mac
`python-dev` should come bundled in with `brews` version of python.
```
brew install ffmpeg 
```

## Running locally
After you have the above dependencies and an api token you will need to export
the api token as an environment variable:

### export api key
```
export DISCORD_API_TOKEN=<your_token>
```

It is highly advisable to create a virtual env:
```
python -m venv .venv
# And then activate the profile
source ./.venv/bin/activate
```

### install python dependencies
```
pip install -r ./requirements.txt
```

### run
```
python ./src/main.py
```