# Parse links (base urls + all params combinations)

```bash
$ head -10 parsers/prehistoric_parsers/zvk/data/elektronika/smartfony
https://zvk.ru/catalog/elektronika/smartfony/filter/smartphone_display-6_2/
https://zvk.ru/catalog/elektronika/smartfony/filter/smartphone_display-6_7/
https://zvk.ru/catalog/elektronika/smartfony/filter/smartphone_display-6_8/
https://zvk.ru/catalog/elektronika/smartfony/filter/smartphone_resolution-6893c3e4723372a49d1687e00dacb4e5/
https://zvk.ru/catalog/elektronika/smartfony/filter/smartphone_resolution-feab75fed5620362eb346fd748996a06/
https://zvk.ru/catalog/elektronika/smartfony/filter/smartphone_operativa-01f3eabd023e178099214c36f420c67d/
https://zvk.ru/catalog/elektronika/smartfony/filter/smartphone_operativa-eb1b648b36573ca11302fed5404ab8a6/
https://zvk.ru/catalog/elektronika/smartfony/filter/smartphone_ram-d847a68ea51eb6ca72154e2afb78d662/
https://zvk.ru/catalog/elektronika/smartfony/filter/smartphone_ram-5c2948525edb223c9fc2611646e7bd20/
https://zvk.ru/catalog/elektronika/smartfony/filter/smartphone_colvocamer-ffde177e5af4bd81de97206a03f4a3a0/
```

```bash
parsers/zvk/data/
├── _all_parsed
├── elektronika
│   └── smartfony
├── kartridzhi
│   ├── obmen-kartridzhey
│   ├── originalnye-kartridzhi
│   ├── sovmestimye-kartridzhi
│   ├── sovmestimye-kartridzhi-zvk
│   └── zapravka-kartridzhey
├── kompyuternoe-oborudovanie
│   ├── bloki-pitaniya
│   ├── kompyutery
│   ├── kompyutery-zvk
│   ├── korpusa
│   ├── kulery
│   ├── materinskie-platy
│   ├── moduli-pamyati
│   ├── monitory
│   ├── monobloki
│   ├── noutbuki
│   ├── protsessory
│   ├── ssd-nakopiteli
│   ├── ustroystva-vvoda-i-manipulyatory
│   ├── videokarty
│   └── zhestkie-diski
├── ofisnye-tovary
│   ├── fotobumaga
│   ├── ofisnaya-bumaga
│   ├── spetsializirovannaya-bumaga
│   └── tovary-dlya-ofisa
├── orgtekhnika
│   ├── arenda-orgtekhniki
│   ├── dopolnitelnye-optsii
│   ├── kopiry-mfu
│   ├── laminatory
│   ├── perepletchiki
│   ├── plottery
│   ├── printery
│   ├── printery-etiketok
│   ├── remont-orgtekhniki
│   ├── rezaki
│   ├── shredery
│   ├── skanery
│   ├── uslugi
│   └── zapchasti
├── prezentatsionnoe-oborudovanie
│   ├── displei-dlya-videosten
│   ├── interaktivnye-displei
│   ├── interaktivnye-doski
│   ├── kommercheskie-televizory
│   ├── proektory
│   ├── professionalnye-paneli
│   └── svetodiodnye-led-paneli-dlya-videosten
├── stopkoronavirus
│   ├── dezinfitsiruyushchie-sredstva
│   ├── maski
│   ├── podstavki-dlya-retsirkulyatorov
│   └── retsirkulyatory
└── televizory-audio-video
    ├── kronshteyny
    └── televizory

8 directories, 53 files
```
#
```sh
	Command being timed: "./.venv/bin/python3 . zvk"
	User time (seconds): 123.61
	System time (seconds): 83.02
	Percent of CPU this job got: 3%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:38:12
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 60876
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 10356
	Minor (reclaiming a frame) page faults: 2249426
	Voluntary context switches: 1133232
	Involuntary context switches: 2221
	Swaps: 0
	File system inputs: 1225624
	File system outputs: 158768
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```
