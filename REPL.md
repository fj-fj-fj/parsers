>>>>>>>>>> <h1 align="center">REPL example</h1>

## Start
```bash
(3.11.0) $ # Run parser 'foo'
(3.11.0) $ make run foo
```
```python
# REPL
Usage
=====
    First start writing CSS selectors
    ---------------------------------

    >>> parser.go
    >>> soup.select(...)
    >>> soup.select_one(...)
    >>> xp.add(<successful string>)
    >>> # ...
    >>> xp.save()
    >>> q()

    Now that you have a list of CSS selectors, just run this parser
    ---------------------------------------------------------------

    Find parsed data in $PROJECT_DIR/data/<parser>
    They are yours.
```

## Parsing
```python
>>> parser.request('https://free-proxy-list.net/')
<Response [200]>
>>> parser.parse()
>>>
HandledData(data="<class 'bs4.BeautifulSoup'>", fail=False)
>>> _
HandledData(data="<class 'bs4.BeautifulSoup'>", fail=False)
>>> 'foo'
'foo'
>>> _
'foo'
>>> HandledData
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
NameError: name 'HandledData' is not defined
>>> # Use underscore like this:
>>> parser._
HandledData(data="<class 'bs4.BeautifulSoup'>", fail=False)
>>> parser.last_result == _
True
>>> # Each method has its own final result
>>> parser.request._
<Response [200]>
>>> parser.parse._
HandledData(data="<class 'bs4.BeautifulSoup'>", fail=False)
>>>
>>> # Collect proxies from soup
>>> soup = _.data
>>> ips = soup.select('table td:nth-of-type(1)')
>>> ips
[...]  # Expectation vs. reality ~ 50%
>>>
>>> ips = soup.select('table td:nth-of-type(1):not(:has([class]))')
>>> # expectation vs reality ~ 90+
>>> ips = soup.select('table td:nth-of-type(1):not(:has([class])):not([class])')
>>> # expectation vs reality ~ 100%
>>>
>>> # Use 'notes' shortcut
>>> nb
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'nb' is not defined
>>> shortcuts()
>>> nb
<function <lambda> at 0x7f834f2853a0>
>> nb == notes
True
>>>
>>> nb.ips = [ip.text for ip in ips]
>>> nb.ips
['47.91.44.217', '34.81.72.31', ... '2022-12-16', '2022-12-15']
>>> # add success selector to `samples`
>>> ss == samples  # use shortcut
True
>>> ss.append('table td:nth-of-type(1):not(:has([class])):not([class])')
>>>
>>> ports = soup.select('table td:nth-of-type(2):not(:has([class])):not([class])')
>>> # expectation vs reality ~ 90+
>>> ports = soup.select('table td:nth-of-type(2):not(:has([class])):not([class]):not([title])')
>>> # expectation vs reality ~ 100%
>>> nb.ports = [port.text for port in ports]
>>> nb.ports
['8000', '80', ... '945', '861']
>>> ss.append('table td:nth-of-type(2):not(:has([class])):not([class]):not([title])')
>>> ss.save() # just in case
>>>
>>> len(nb.ips), len(nb.ports)
(305, 305)
>>> # at least for this
>>> import datetime as d; d.datetime.now()
datetime.datetime(2022, 12, 20, 0, 26, 48, 467282)
>>>
>>> # Collect proxies
>>> nb.f = lambda: [f'{ip}:{port}' for ip,port in zip(nb.ips, nb.ports)]
>>> nb.f()
['47.91.44.217:8000', '34.81.72.31:80', [...] '2022-12-16:945', '2022-12-15:861']
>>> nb.proxies = _
>>>
>>> nb()
{'ips': ['96.126.103.64', ... '2022-12-15'],
'ports': ['9992', '80', '80', '3128', ... '861'],
'func': <function <lambda> at 0x7f834f287380>,
'proxies': ['96.126.103.64:9992', ... '2022-12-15:861']}
>>> # OK
```

## Saving
```python
>>> # Save your samples
>>> ss.save()
>>> # Your notes will be automatically saved to parsers/user_parsers/<parser>/notes.txt
>>> q()
```

## Reloading
```python
>>>
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
  reloading 'parsers.user_parsers.foo.config'...               [ok]
  reloading 'parsers.user_parsers.foo.constants'...            [ok]
  reloading 'parsers.user_parsers.foo.parser'...               [ok]
  reloading 'parsers.user_parsers.foo'...                      [ok]
  └── 13 modules successfully reloaded


>>>
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

## Shortcuts
```python
>>>
>>> fn
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'f' is not defined
>>> shortcuts()
>>> fn
<function main at 0x7f27834f91c0>
>>> # See more in parsers.imports.shortcuts
```
