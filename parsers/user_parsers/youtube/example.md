```bash
(3.11.0) $ make irun youtube
```
```python
>>> # https://pytube.io/en/latest/user/install.html#get-the-source-code
>>>
>>> parser.request()
<Playlist [type='Sequence', len=12]>
>>> shortcuts()
>>> _
<Playlist [type='Sequence', len=12]>
>>> _.json()
['https://www.youtube.com/watch?v=-py9GXvJk6A', 'https://www.youtube.com/watch?v=VrShEItN0Jc', 
'https://www.youtube.com/watch?v=rkjg71GJPvA', 'https://www.youtube.com/watch?v=VY95vgOROo8', 
'https://www.youtube.com/watch?v=kmdA7zJS9gw', 'https://www.youtube.com/watch?v=2pttEjdYJuo', 
'https://www.youtube.com/watch?v=a6UtrJ4Xh-Y', 'https://www.youtube.com/watch?v=Xxuy1zFCMhc', 
'https://www.youtube.com/watch?v=x6JZmBK2I8Y', 'https://www.youtube.com/watch?v=czqYT7103Eo', 
'https://www.youtube.com/watch?v=VomXaukdWxo', 'https://www.youtube.com/watch?v=ISo-L-0xsoI']
>>> nb.playlist_videos = _
>>>
>>> dir(parser.request._)
['_NoAutoResponse__dtype', '_NoAutoResponse__r', '__attrs__', '__bool__', '__class__', 
'__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', 
'__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', 
'__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', 
'__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
'__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_content', 
'_content_consumed', '_next', '_ok', 'apparent_encoding', 'close', 'content', 'cookies', 
'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 
'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 
'reason', 'request', 'status_code', 'text', 'url']
>>> parser.request.url
>>> 
>>> dir(parser.request._._NoAutoResponse__r)
['__abstractmethods__', '__class__', '__class_getitem__', '__contains__', '__delattr__', 
'__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', 
'__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', 
'__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', 
'__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__slots__', 
'__str__', '__subclasshook__', '__weakref__', '_abc_impl', '_build_continuation_url', 
'_extract_videos', '_html', '_initial_data', '_input_url', '_paginate', '_playlist_id', 
'_sidebar_info', '_video_url', '_ytcfg', 'count', 'description', 'html', 'index', 
'initial_data', 'last_updated', 'length', 'owner', 'owner_id', 'owner_url', 'playlist_id', 
'playlist_url', 'sidebar_info', 'title', 'trimmed', 'url_generator', 'video_urls', 
'videos', 'videos_generator', 'views', 'yt_api_key', 'ytcfg']
>>> playlist.playlist_url
'https://www.youtube.com/playlist?list=PLlb7e2G7aSpQhNphPSpcO4daaRPeVstku'
>>>
>>> nb.FIXME = (parser.request._._NoAutoResponse__r, 'This object is hidden too far')
>>> playlist = parser.request._._NoAutoResponse__r
>>>
>>> # create download directory
>>> playlist._playlist_id
'PLlb7e2G7aSpQhNphPSpcO4daaRPeVstku'
>>> download_dir = './data/youtube/' + _
>>> download_dir
'./data/youtobe/PLlb7e2G7aSpQhNphPSpcO4daaRPeVstku'
>>> nb.download_dir = _
>>> import os
>>> os.mkdir(download_dir)
>>> os.listdir('./data/youtube')
['PLlb7e2G7aSpQhNphPSpcO4daaRPeVstku', 'repl_1_response.html',]
>>>
>>> # main
>>> for video in playlist.videos:
...     video.streams.filter(type='video', progressive=True, file_extension='mp4').\
...     order_by('resolution').desc().first().download(download_dir)
...
[...]
>>>
>>> for i in os.listdir(download_dir): i
...
'Лекция 1 Программирование на Python.mp4'
'Лекция 10 Классы II (Программирование на Python).mp4'
'Лекция 11 Тестирование (Программирование на Python).mp4'
'Лекция 12 Модули (Программирование на Python).mp4'
'Лекция 2 Функции.mp4'
'Лекция 3 Декораторы (Программирование на Python).mp4'
'Лекция 4 Строки байты IO (Программирование на Python).mp4'
'Лекция 5 Коллекции и collections (Программирование на Python).mp4'
'Лекция 6 Классы I (Программирование на Python).mp4'
'Лекция 7 Работа с исключениями (Программирование на Python).mp4'
'Лекция 8 Итераторы (Программирование на Python).mp4'
'Лекция 9 async  await (Программирование на Python).mp4'
>>>
```
```bash
# move downloaded from C to D (with WSL)
./parsers/user_parsers/youtube/mv_to_d.sh 1
```
