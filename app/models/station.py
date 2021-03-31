class Station:
    '''
    Station class which represents a mrt station.
    '''
    def __init__(self, id: str, name: str, open_date: str):
        self.id = id
        self.line = id[:2]
        self.name = name
        self.open_date = open_date
        self.next = []

    def __lt__(self, s2):
        return self.name < s2.name

    def __repr__(self):
        return f'Station({self.id}, {self.name}, {self.open_date}, {self.next})'

    def __str__(self):
        return f'(id:{self.id}, name:{self.name}, open_date:{self.open_date})'