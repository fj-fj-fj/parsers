>>>>>>>> <h1 align="center">REPL example</h1>

## Start
```bash
(3.11.0) $ create_parser foo

Template 'foo' created successfully.

/path-to-repo/parsers/user_parsers/foo
├── [-rwxrwxrwx]  __init__.py
├── [-rwxrwxrwx]  constants.py
├── [-rwxrwxrwx]  logic.py
├── [-rwxrwxrwx]  notes.txt
├── [-rwxrwxrwx]  parser.py
└── [-rwxrwxrwx]  samples.txt

0 directories, 6 files
(3.11.0) $ # Run parser 'foo' (see Makefile)
(3.11.0) $ make irun foo
```
```python
# REPL
Usage:

    First start writing CSS selectors
    ---------------------------------

    >>> parser.go
    >>> soup.select(<any selector>)
    >>> ss.add(<correct selector>)
    >>> # ... See more EXAMPLE.md
    >>> ss.save()
    >>> q()

    Now that you have a list of samples, just run this parser
    ---------------------------------------------------------

    Find parsed data in /mnt/c/dev/fj-fj-fj/parsers/data/<parser>
    They are yours.


>>>
```

## Parsing
```python
>>> # import os; assert os.listdir('./data/foo') == []
>>>
>>> __parser__.constants.URL
'https://foo.com/'
>>> # This site is not interesting
>>> # We came up with a bad name. Change the url
>>> parser.request('https://free-proxy-list.net/')
<Response [200]>
>>> # assert os.listdir('./data/foo') == ['repl_1_response.html']
>>>
>>> parser.parse()
HandledData(data=<class 'bs4.BeautifulSoup'>, fail=False, status_code=0)
>>> # assert os.listdir('./data/foo') == ['repl_1_raw_data.tmp', 'repl_1_response.html']
>>> _
HandledData(data=<class 'bs4.BeautifulSoup'>, fail=False, status_code=0)
>>> 'foo'
'foo'
>>> _
'foo'
>>> HandledData
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
NameError: name 'HandledData' is not defined
>>>
>>> parser._
HandledData(data=<class 'bs4.BeautifulSoup'>, fail=False, status_code=0)
>>> parser.last_result == _
True
>>> # Each method has its own final result
>>> parser.request._
<Response [200]>
>>> parser.parse._
HandledData(data=<class 'bs4.BeautifulSoup'>, fail=False, status_code=0)
>>>
>>> # Collect proxies from soup
>>> soup = _.data
>>> ips = soup.select('table td:nth-of-type(1)')
>>> ips
[...]  # Expectation vs. reality ~50%
>>>
>>> ips = soup.select('table td:nth-of-type(1):not(:has([class]))')
>>> # ^ expectation vs reality ~90%
>>> ips = soup.select('table td:nth-of-type(1):not(:has([class])):not([class])')
>>> # ^ 100% match
>>>
>>> # Saving a few keystrokes
>>> # Use 'notes' shortcut
>>> nb
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'nb' is not defined
>>> shortcuts()
>>> nb
<function <lambda> at 0x7f834f2853a0>
>> nb == note
True
>>>
>>> # Store ips as a function attribute to avoid reassignment and history digging
>>> nb.ips = [ip.text for ip in ips if '.' in ip.text]
>>> nb.ips
['169.57.1.85:8123', '18.136.21.248', ... '154.236.184.71', '89.107.197.164']
>>> # Use 'less' for paging through text one screenful at a time
>>> parser.less(nb.ips) # q
>>>
>>> # add success selector to `samples`
>>> ss == samples  # (shortcut)
True
>>> ss.append('table td:nth-of-type(1):not(:has([class])):not([class])')
>>>
>>> ports = soup.select('table td:nth-of-type(2):not(:has([class])):not([class])')
>>> # ^ expectation vs reality ~90%
>>> ports = soup.select('table td:nth-of-type(2):not(:has([class])):not([class]):not([title])')
>>> # ^ 100% match
>>> nb.ports = [port.text for port in ports]
>>> nb.ports
['8123', '8118', ... '707', '770']
>>> ss.append('table td:nth-of-type(2):not(:has([class])):not([class]):not([title])')
>>>
>>> len(nb.ips), len(nb.ports)
(300, 305)  # skip 5 no-ip items
>>>
>>> import datetime as d; d.datetime.now()
datetime.datetime(2023, 1, 2, 13, 29, 39, 8729)
>>>
>>> # Create sample handler function and collect proxies
>>> nb.sample_handler = lambda: [f'{ip}:{port}' for ip,port in zip(nb.ips, nb.ports)]
>>> nb.proxies = nb.sample_handler()
>>> nb.proxies
['169.57.1.85:8123', '18.136.21.248:8118', ... '154.236.184.71:1975', '89.107.197.164:3128']
>>>
>>> parser.less(nb())
# {'ips': ['169.57.1.85', ... '89.107.197.164'],
# 'ports': ['8123', '8118', ... '707', '770'],
# 'sample_handler': <function <lambda> at ...>,
# 'proxies': ['169.57.1.85:8123', ... '89.107.197.164:3128']}
# (END)
```

## Saving
```python
>>> # Save your samples
>>> ss.save()
>>> # Your notes will be automatically saved to parsers/user_parsers/<parser>/notes.txt
>>> quit()  # Follow next header
>>> # Or make final data manually
>>> parser.handler._data_handler.samples = ss
>>> parser.handler._data_handler.sample_handler = lambda x: [f'{i}:{p}' for i,p in zip(x[0], x[1])]
>>> final_data = parser.handler._data_handler.prepare()
>>> parser.save()
6639
>>> # assert os.listdir('./data/foo')[0] == 'repl_1_final_data.json'
```

- ./parsers/user_parsers/foo/notes.txt is enough to quickly work with data.
- To run the parser regularly, add sample handler and restart in normal mode

### Add sample handler to ./parsers/user_parsers/foo/logic.py
```diff
def main(samples: list[list[Ip], list[Port]]) -> Proxies:
    """Handle samples. (API)"""
+   return collect_proxies(*samples)
+
+def collect_proxies(ips, ports):
+    return [collect_proxy(ip, port) for ip, port in zip(ips, ports)]
+
+def collect_proxy(ip, port):
+    return f'{ip}:{port}'
```

### Fix url in ./parsers/user_parsers/foo/constants.py
* in this case it's necessary
```diff
# Delete condition or reassign `URL`
if 000 not in range(200, 400):
-    URL = _base.URL.HTTPBIN_ORG
+    URL = 'https://free-proxy-list.net'
```

## Start with samples
```bash
(3.11.0) $ # Run parser with ./parsers/user_parsers/foo/logic.py
(3.11.0) $ make run foo
(3.11.0) $ # Finish!
```

## Check final data
```bash
(3.11.0) $ ls -a ./data/foo
.   1_final_data.json  1_response.html         repl_1_raw_data.tmp
..  1_raw_data.tmp     repl_1_final_data.json  repl_1_response.html
(3.11.0) $
(3.11.0) $ wc !$/1_final_data.json
wc ./data/foo/1_final_data.json
   0  305 6591 ./data/foo/1_final_data.json
(3.11.0) $
(3.11.0) $ jq '. | first' !$
jq '. | first' ./data/foo/1_final_data.json
"96.126.124.197:52725"
```


# Some more repl

## Shortcuts
```python
>>> # Abbreviate base entities to make their usage less verbose
>>> fn
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'f' is not defined
>>> shortcuts()
>>> fn
<function main at 0x7f27834f91c0>
>>> # See more in parsers.imports.shortcuts
```

## Reloading
```python
>>> refresh()
  reloading 'parsers.imports'...                               [ok]
  reloading 'parsers.user_parsers'...                          [ok]
  reloading 'parsers.datatypes'...                             [ok]
  reloading 'parsers.exceptions'...                            [ok]
  reloading 'parsers.constants'...                             [ok]
  reloading 'parsers.storage'...                               [ok]
  reloading 'parsers.interfaces'...                            [ok]
  reloading 'parsers.storage.files'...                         [ok]
  reloading 'parsers.handlers'...                              [ok]
  reloading 'parsers.user_parsers.foo.constants'...            [ok]
  reloading 'parsers.user_parsers.foo.logic'...                [ok]
  reloading 'parsers.user_parsers.foo.parser'...               [ok]
  reloading 'parsers.user_parsers.foo'...                      [ok]
  └── 13 modules successfully reloaded


>>> __parser__.__name__
'parsers.user_parsers.foo'
>>>
>>> refresh(pkg=__parser__)
<function refresh.<locals>.refresh_user_parser_package.<locals>.reload at 0x7f934d2891c0>
>>> _refresh(pkg=__parser__)()
reloading 'parsers.user_parsers.foo'...
- 'parsers.user_parsers.foo' successfully reloaded


>>> refresh(pkg='parser')()
reloading 'parsers.user_parsers.foo'...
- 'parsers.user_parsers.foo' successfully reloaded

```
