import pytest
from exceptions import InvalidArgumentError
from record_storage import RecordStorage
from state_store_service import EventDescriptor

def test_constructor_with_dataset_name():
    expected_dataset = 'record_dataset_name'
    record_storage = RecordStorage(expected_dataset)

    assert record_storage.dataset_name == expected_dataset 

def test_constructor_without_dataset_name():
    record_storage = RecordStorage()

    assert record_storage.dataset_name == 'unknown'

def test_record_fails_because_breakpoint_is_none():
    record_storage = RecordStorage()

    with pytest.raises(InvalidArgumentError):
        record_storage.record(breakpoint=None, key=None, value=None)


def test_record_and_iterate_successfully():
    record_storage = RecordStorage()

    event_descriptor = EventDescriptor(0, 0, None, None, 0, None, None) 

    record_storage.record(breakpoint=event_descriptor, key='', value=None)
    record_storage.record(breakpoint=event_descriptor, key='', value=None)

    assert len(record_storage.iterate()) == 2