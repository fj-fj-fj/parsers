# Youtube playlist downloader

Sometimes great audio/video(s) become unavailable.<br>
May the best of them be saved.

#
## Add playlist ID to ./constants.py and start
Download mp4 videos into $PROJECT_DIR/data/youtube/<PLAYLIST_ID>
```bash
make run youtube
```

## Move downloaded to smth
Update ./playlists
```json
{
    // replace kyes, values
    "N": "desired playlist ID",
    "N_move_to": "destination direcroty"
}
```
Run script
```bash
./move.sh <N>
```

#
## Requirements
```bash
pip install pytube
```
To convert downloaded audio to mp3
```bash
pip install ffmpy
```
Or just
```bash
# (3.11.0) $ uncomment whatever you need and call pip
pip install -r ./requirements.txt
```
