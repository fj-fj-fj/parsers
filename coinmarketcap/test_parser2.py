# 1. Test query 'SELECT * FROM coinmarketcap;'
# 2. pretty output in terminal

class Test:
    """Output color query in the terminal.
    
    Before referring to the database,
    transfer the session and table before.

    :session: sqlalchemy.orm.session.Session
    :table: sqlalchemy.ext.declarative.api.DeclarativeMeta

    """
    RESET = '\33[0m'
    BOLD='\033[01m'
    GRAY = '\33[2m'
    RED = '\33[31m'
    YELLOW = '\33[33m'
    VIOLET = '\33[35m'
    CYAN = '\033[36m'
    BG_BLACK = '\33[40m'

    SESSION = None
    TABLE = None
    
    @staticmethod
    def _body():
        """Print body (id, name, ticker, price, source)"""
        query = Test.SESSION.query(Test.TABLE).order_by()
        for q in query.all():
            print(f'{Test.BG_BLACK}{str(q.id).zfill(3)}', end='')
            print(f'{Test.YELLOW}{q.name.rjust(25)}', end='')
            print(f' {Test.GRAY}{Test.BOLD}{q.ticker.ljust(6)}{Test.RESET}', end='\t')
            print(f'{Test.VIOLET}{str(q.price).center(8)}', end='\t')
            print(f'{Test.CYAN}{q.source.ljust(50)}{Test.RESET}')
            
    @staticmethod
    def _head():
        """Print title (index, name, ticker, price, url)"""
        print(f"\n{Test.RED}index {'name'.rjust(22)} {'ticker'.ljust(6)}", end='\t')
        print(f"{'price'.center(8)}\t{'url'.ljust(10)}{Test.RESET}")

    @staticmethod
    def all():
        Test._head()
        Test._body()
