class Result(object):
    __slots__ = ('flag', 'time', 'real_time', 'memory', 'output', 'points')

    AC = 0
    WA = 1 << 0
    RTE = 1 << 1
    TLE = 1 << 2
    MLE = 1 << 3
    IR = 1 << 4
    SC = 1 << 5
    OLE = 1 << 6
    IE = 1 << 30

    def __init__(self):
        self.flag = 0
        self.time = 0
        self.real_time = 0
        self.memory = 0
        self.output = ''
        self.points = 0