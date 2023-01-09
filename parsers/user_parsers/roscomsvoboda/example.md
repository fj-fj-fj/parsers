# Flow

## Repl work
```bash
(3.11.0) $ make irun roscomsvoboda
```
```python
>>> parser.request()
<Response [200]>
>>> parser.parse()
HandledData(data=<class 'list'>, fail=False, status_code=0)
>>>
>>> f = lambda key: key.split('.')[-1]
>>> f('foo.io')
'io'
>>> blocked_sites = parser.parse._.data
>>> len(blocked_sites)
136852
>>> blocked_sites[0]
'0-00.lordfilm0.biz'
>>> f(_)
'biz'
>>>
>>> shortcuts()
>>> nb.get_toplvl_domain = f
>>> 
>>> from itertools import groupby
>>> grouped = [{fd: list(urls)} for fd,urls in groupby(sorted(blocked_sites, key), key)]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'key' is not defined
>>> key = f
>>> grouped = [{fd: list(urls)} for fd,urls in groupby(sorted(blocked_sites, key), key)]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: sorted expected 1 argument, got 2
>>>
>>> grouped = [{fd: list(urls)} for fd,urls in groupby(sorted(blocked_sites, key=f), key=f)]
>>> grouped[0]
{'ac': ['anticarder.ac', 'bdf.ac', 'cccc.ac', 'filmec.ac', 'filmitorrent.unblocked.ac', 'filmix.ac', 'fog.ac', 'harlem.ac', 'kinogo.unblocked.ac', 'kinosimka.unblocked.ac', 'light-trading.umarkets.ac', 'lordfilm.ac', 'prtrend.ac', 'rutor.ac', 'stake.ac', 'stream.crichd.ac', 'umarkets.ac']}
>>> len(grouped)
460
>>>
>>> lvls = {}
>>> for d in grouped: lvls |+ d
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: bad operand type for unary +: 'dict'
>>> for d in grouped: lvls |= d
...
>>> lvls.keys()
dict_keys(['ac', 'academy', 'actor', 'adult', 'ae', 'af', 'africa', 'ag', 'agency', 'ai', 'al', 'am', 'app', 'ar', 'army', 'art', 'as', 'asia', 'at', 'au', 'auction', 'audio', 'autos', 'ba', 'baby', 'band', 'bar', 'bd', 'be', 'beauty', 'beer', 'best', 'bf', 'bg', 'bid', 'bike', 'bio', 'biz', 'black', 'blog', 'blue', 'bo', 'bond', 'boutique', 'br', 'broker', 'business', 'buzz', 'bw', 'by', 'bz', 'ca', 'cab', 'cam', 'camp', 'cards', 'care', 'cat', 'cc', 'cd', 'center', 'ceo', 'cf', 'cfd', 'ch', 'chat', 'cheap', 'ci', 'city', 'cl', 'click', 'clinic', 'cloud', 'club', 'cm', 'cn', 'co', 'codes', 'com', 'community', 'company', 'consulting', 'contact', 'cool', 'coop', 'country', 'cr', 'cx', 'cy', 'cyou', 'cz', 'dance', 'date', 'dating', 'day', 'de', 'deals', 'delivery', 'democrat', 'desi', 'design', 'dev', 'diamonds', 'digital', 'direct', 'directory', 'dj', 'dk', 'dm', 'do', 'dog', 'download', 'ec', 'edu', 'education', 'ee', 'eg', 'email', 'energy', 'es', 'estate', 'eu', 'events', 'exchange', 'expert', 'express', 'fail', 'faith', 'family', 'fan', 'fans', 'farm', 'fashion', 'fi', 'film', 'finance', 'financial', 'fit', 'fitness', 'florist', 'fm', 'fo', 'football', 'foundation', 'fr', 'frl', 'fun', 'fund', 'futbol', 'fyi', 'ga', 'gallery', 'game', 'games', 'garden', 'gay', 'gd', 'gdn', 'ge', 'gg', 'gift', 'gifts', 'gives', 'gl', 'global', 'golf', 'gov', 'gq', 'gr', 'graphics', 'gratis', 'gree', 'green', 'group', 'gs', 'guide', 'guru', 'hair', 'haus', 'health', 'healthcare', 'help', 'hk', 'hm', 'holdings', 'homes', 'horse', 'hospital', 'host', 'house', 'how', 'hr', 'ht', 'hu', 'icu', 'id', 'ie', 'il', 'im', 'immo', 'in', 'inc', 'industries', 'info', 'ink', 'insure', 'international', 'io', 'ir', 'irish', 'is', 'it', 'jp', 'jpg', 'kaufen', 'ke', 'kg', 'kim', 'kiwi', 'kr', 'kw', 'ky', 'kz', 'la', 'land', 'lat', 'lb', 'lc', 'legal', 'lgbt', 'li', 'lib', 'lic', 'life', 'limited', 'limo', 'link', 'live', 'llc', 'loan', 'lol', 'london', 'love', 'lt', 'ltd', 'lu', 'lv', 'ly', 'ma', 'makeup', 'market', 'marketing', 'markets', 'mba', 'md', 'me', 'media', 'men', 'menu', 'mg', 'miami', 'mk', 'ml', 'mob', 'mobi', 'moda', 'moe', 'mom', 'monster', 'moscow', 'movie', 'mp', 'ms', 'mx', 'my', 'mz', 'name', 'ne', 'net', 'network', 'news', 'nf', 'ng', 'ninja', 'nl', 'no', 'np', 'nu', 'nz', 'observer', 'one', 'onl', 'onlin', 'ooo', 'or', 'org', 'ovh', 'page', 'partners', 'party', 'pe', 'pet', 'ph', 'photo', 'photos', 'pics', 'pictures', 'pink', 'pizza', 'pk', 'pl', 'place', 'plus', 'pm', 'pn', 'porn', 'press', 'pro', 'promo', 'ps', 'pt', 'pub', 'pw', 'qpon', 'qtx-market', 'quest', 'radio', 're', 'realrty', 'realty', 'red', 'ren', 'rent', 'report', 'rest', 'reviews', 'rip', 'ro', 'rocks', 'rodeo', 'rs', 'ru', 'ru/', 'run', 'sale', 'sb', 'sbs', 'sc', 'school', 'science', 'se', 'sex', 'sexy', 'sg', 'sh', 'shop', 'shopping', 'show', 'si', 'site', 'sk', 'skin', 'so', 'soccer', 'social', 'solar', 'solutions', 'soy', 'space', 'st', 'store', 'stream', 'studio', 'study', 'style', 'su', 'support', 'surf', 'sx', 'systems', 'tatar', 'tattoo', 'tax', 'taxi', 'team', 'tech', 'technology', 'tel', 'tf', 'tg', 'th', 'tips', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'today', 'tools', 'top', 'town', 'tr', 'trade', 'trading', 'travel', 'tube', 'tv', 'tw', 'tz', 'ua', 'ug', 'uk', 'uno', 'us', 'uy', 'uz', 'vc', 've', 'ventures', 'vet', 'vg', 'video', 'vin', 'vision', 'vn', 'vodka', 'vote', 'vu', 'wales', 'wang', 'watch', 'webcam', 'website', 'wf', 'wiki', 'win', 'wine', 'work', 'works', 'world', 'ws', 'wtf', 'xn--80adxhks', 'xn--80asehdb', 'xn--80aswg', 'xn--90ais', 'xn--c-7tb', 'xn--c1avg', 'xn--d1acj3b', 'xn--j1amh', 'xn--p1acf', 'xn--p1ai', 'xn--q1aa', 'xxx', 'xyz', 'yoga', 'yt', 'za', 'zone'])
>>>
>>> nb.groupby = "[{fd: list(urls)} for fd,urls in groupby(sorted(blocked_sites, key=nb.get_toplvl_domain), key=nb.get_toplvl_domain)]"
>>> nb.lvls = lvls.keys()
>>> nb.grouped = f'''
... {grouped[0]}
...
...     ...
...
... {grouped[-1]}'''
>>>
```

## constants/logic work
```bash
(3.11.0) $ make run roscomsvoboda
```
