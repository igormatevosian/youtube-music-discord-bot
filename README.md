# Discord Music Bot

This is a Discord bot that plays music from YouTube in voice channels. The bot uses `discord.py` for interacting with Discord and `yt-dlp` for downloading and streaming audio.

## Features

- Play music from YouTube.
- Pause, resume, stop, and skip tracks.
- Display the current queue of tracks.

## Prerequisites

- Python 3.8 or higher
- A Discord account
- A Discord bot token
- `ffmpeg` installed and added to `PATH`

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/letsmol/youtube-music-discord-bot
    cd discord-music-bot
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Install `ffmpeg`:
    - **Windows**:
        1. Download `ffmpeg` from [ffmpeg.org](https://ffmpeg.org/download.html).
        2. Extract the downloaded file to a directory.
        3. Add the `bin` directory to your system `PATH`.

    - **MacOS**:
        ```sh
        brew install ffmpeg
        ```

    - **Linux**:
        ```sh
        sudo apt update
        sudo apt install ffmpeg
        ```

5. Create a `config.yaml` file in the root directory of the project and add your bot token and other configurations:
    ```yaml
    TOKEN: YOUR_DISCORD_BOT_TOKEN
    command_prefix: /
    tracks_dir: tracks
    ```

## Usage

1. Run the bot:
    ```sh
    python main.py
    ```

2. Use the following commands in a Discord server where the bot is present:
    - `/play <url>`: Play a song from YouTube.
    - `/pause`: Pause the current song.
    - `/resume`: Resume the paused song.
    - `/stop`: Stop the current song and clear the queue.
    - `/skip`: Skip the current song.
    - `/queued`: Display the queue of songs.
    - `/leave`: Make the bot leave the voice channel.

## Configuration

The bot is configured using the `config.yaml` file. The available configurations are:

- `TOKEN`: The bot token obtained from the Discord Developer Portal.
- `command_prefix`: The prefix for bot commands.
- `tracks_dir`: The directory where downloaded tracks will be saved.

## Example

Here is an example of the `config.yaml` file:

```yaml
TOKEN: YOUR_DISCORD_BOT_TOKEN
command_prefix: /
tracks_dir: tracks
