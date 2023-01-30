# Youtube video(s) downloader

Sometimes great audio/video(s) become unavailable.<br>
May the best of them be saved.

#
## Prestart steps
### ./constants.py
- Add constant with video or playlist ID
- Configure URL `PARAMS`
- For more information see `__doc__` of the module
### ./parser.py
- Select `sample_handler`
- To download one video select `use.yt`
- To download playlist select `use.pl`
- For more information see `__doc__` of the module

#
## Run
```bash
make run youtube
```
Check downloaded in `$PROJECT_DIR/data/youtube/`

#
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
