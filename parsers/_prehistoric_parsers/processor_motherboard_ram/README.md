# Parse characteristics of motherboards and processors

Name, Brand, Maximum memory, PCI Express version, Integrated graphics core, Package weight (units), Warranty

## Parsed data
```bash
$ head -10 ./data/materinskie-platy.csv ./data/processory.csv
```
```
==> ./data/materinskie-platy.csv <==
Наименование,Бренд,Чипсет,Тип поддерживаемой памяти,Слотов PCI-E x1,Разъемов SATA3,Разъем PS/2,Сетевой интерфейс,Форм-фактор,Габариты упаковки (ед) ДхШхВ,Гарантия
"материнская плата MSI H510M-A PRO, LGA 1200, Intel H510, mATX, Ret",MSI,Intel H510,DIMM,1,4,1 шт. (клавиатура или мышь),Gigabit Ethernet,mATX,0.26x0.26x0.06 м,36 мес.
"материнская плата GIGABYTE H510M H, LGA 1200, Intel H510, mATX, Ret",GIGABYTE,Intel H510,DIMM,1,4,1 шт. (клавиатура или мышь),Gigabit Ethernet,mATX,0.83 кг,36 мес.
"материнская плата ASUS PRIME H510M-K, LGA 1200, Intel H510, mATX, Ret",ASUS,Intel H510,DIMM,1,4,1 шт. (клавиатура или мышь),Gigabit Ethernet,mATX,0.27x0.26x0.05 м,36 мес.

==> ./data/processory.csv <==
Наименование,Брэнд,Максимальный объем памяти,Версия PCI Express,Встроенное графическое ядро,Вес упаковки (ед),Гарантия
"процессор Intel Core i5 11400F, LGA 1200,  OEM",INTEL,128 ГБ,PCI Express 4.0,отсутствует,0.039 кг,12 мес.
"процессор Intel Core i5 12400F, LGA 1700,  OEM",INTEL,128 ГБ,PCI Express 5.0,отсутствует,0.053 кг,12 мес.
"процессор Intel Core i3 10100F, LGA 1200,  OEM",INTEL,128 ГБ,PCI Express 3.0,отсутствует,0.029 кг,12 мес.
"процессор Intel Core i3 12100F, LGA 1700,  OEM",INTEL,128 ГБ,PCI Express 5.0,отсутствует,0.053 кг,12 мес.
"процессор AMD Ryzen 5 5600X, SocketAM4,  OEM [100-000000065]",AMD,128 ГБ,PCI Express 4.0,отсутствует,0.102 кг,12 мес.
"процессор AMD Ryzen 5 3600, SocketAM4,  OEM [100-000000031]",AMD,DDR4,PCI Express 4.0,отсутствует,0.08 кг,12 мес.
"процессор Intel Core i3 10105F, LGA 1200,  OEM",INTEL,128 ГБ,PCI Express 3.0,отсутствует,0.04 кг,12 мес.
"процессор Intel Core i3 10105, LGA 1200,  OEM",INTEL,128 ГБ,PCI Express 3.0,есть,0.039 кг,12 мес.
"процессор Intel Core i5 10400F, LGA 1200,  OEM",INTEL,128 ГБ,PCI Express 3.0,отсутствует,0.035 кг,12 мес.
```
