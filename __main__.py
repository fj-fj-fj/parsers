import sys

parser = sys.argv[1:] and sys.argv[1:][0]

match parser:
    case 'coinmarketcap':
        parser_number = sys.argv[2]
        match parser_number:
            case '1':
                from parsers.coinmarketcap import *
            case '2':
                from parsers.coinmarketcap import *
    case 'discontinued_tech':
        from parsers.discontinued_tech import *
    case 'zvk':
        from parsers.zvk.links_parser import *
    case _:
        print(f"NameError: name '{parser}' is not defined")
