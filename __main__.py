from sys import argv

parser = argv[1:] and argv[1:][0]

match parser:
    case 'coinmarketcap':
        parser_number = sys.argv[2]
        match parser_number:
            case '1':
                from parsers.coinmarketcap import *
            case '2':
                from parsers.coinmarketcap import *
    case 'ctlnk':
        from parsers.ctlnk.parser import *
    case 'discontinued_tech':
        from parsers.discontinued_tech import *
    case 'zvk':
        from parsers.zvk.links_parser import *
    case 'wiki':
        from parsers.wiki.parse_wikipedia import *
    case _:
        exit(f"NameError: name '{parser}' is not defined!")

# save HTML files localy if needed
if argv[-1] == '--save':
    import os

    directory = f'parsers/{parser}/html'

    if not os.path.exists(directory):
        os.makedirs(directory)

    for link in url.endpoints():
        file = f"{directory}/{link.split('/')[-2]}.html"
        with open(file, 'w') as f:
            f.write(requests.get(link).text)
    exit('- html files saved succesfully!')

# run the main function of the matched parser
main()
