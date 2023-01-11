from collections import namedtuple
from exceptions import InvalidArgumentError
from datetime import datetime

RecordRow = namedtuple(
    'RecordRow',
    ['key', 'breakpoint', 'value', 'datetime'])

RecordRowBreakpoint = namedtuple(
    'RecordRowBreakpoint',
    ['id', 'file', 'line', 'method'])


class RecordStorage:
    '''
    Represents in memory record data storage to keep event query
    results during recording.
    '''

    def __init__(self, dataset_name=None):
        self._data = []
        self.dataset_name = dataset_name if dataset_name is not None else 'unknown'

    def record(self, breakpoint, key, value):
        '''
        Saves a record at the breakpoint.
        Record has to happen at certain event descriptor since it is set
        to breakpoint.
        '''
        if breakpoint is None:
            raise InvalidArgumentError 

        self._data.append(
            RecordRow(
                key=key,
                breakpoint=RecordRowBreakpoint(
                    id=breakpoint.request_id,
                    file=breakpoint.source,
                    line=breakpoint.line_number,
                    method=breakpoint.method_name
                ),
            value=value,
            datetime=datetime.utcnow()))

    def iterate(self):
        return self._data

    def clear(self):
        self._data = self.dataset_name = None