<p align="center">
  <img src="src/resources/gtr_logo.png" />
</p>

# Grand Theft Radio
Discord radio bot able to play any radio station from all GTA games. Only for private discord use currently and not hosted anywhere.

**Note:** Repo does not contain any of the audio files due to limits in Git Storage. Please contact me if you'd like access. 

## Features

* Ability to play all 127 radio stations across 12 games, from GTA 1 to GTA Online in a discord voice channel
* Playback simulates a radio with time based audio streaming
* Search commands for finding a specific station, genre or GTA title

---

## Dev Requirements

* Python >= 3.8

* Poetry

If you want to create the venv in-repo (for IDE detection):

`poetry config virtualenvs.in-project true`


Install dependencies:

`poetry install`

Run the bot:

`poetry run python src/main.py`

