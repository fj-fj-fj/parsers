PARSER = gibdd.py

run:
	python3 -i $(PARSER)

style:
	flake8 .

sort:
	isort .

types:
	mypy .

check:
	make style sort types

REGION = 65
PER_PAGE = 100
URL = 'https://xn--90adear.xn--p1ai/news/region?perPage=$(PER_PAGE)&page=1&region=$(REGION)'

html:
	python3 -c "import requests;\
	from base_config import HEADERS, URL;\
	f=open('data/index.html', 'w', encoding='utf-8');\
	f.write(requests.get(url=URL, headers=HEADERS).text);\
	f.close()"

json:
	python3 -c "import json, requests;\
	from base_config import HEADERS;\
	data=requests.get(url=$(URL), headers=HEADERS).json();\
	f=open('data/$(PER_PAGE)_posts_$(REGION).json', 'w', encoding='utf-8');\
	json.dump(data, f, indent=4, ensure_ascii=False);\
	f.close()"
