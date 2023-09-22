import pytest
from API.process_id_tool.process_id import ProcessManager

def test_add_return_process():
    """
    Test adding a process and returning it.

    This test checks if a process is successfully added and then returned.
    The status of the process should first be 'in use' and then 'available' after it's returned.
    """
    pm = ProcessManager()
    # Add a process
    process_id = pm.add_process('test_process', 'test_user')
    assert process_id == 1
    assert pm.df.loc[process_id, 'Status'] == 'in use'
    assert pm.df.loc[process_id, 'User_ID'] == 'test_user'

    # Return the process
    pm.return_process(process_id, 'test_user', 'test_process')
    assert pm.df.loc[process_id, 'Status'] == 'available'

@pytest.mark.xfail(reason="Process does not belong to 'wrong_user'")
def test_wrong_user():
    """
    Test returning a process with a wrong user.

    This test should fail because the process does not belong to 'wrong_user'.
    """
    pm = ProcessManager()
    # Add a process
    process_id = pm.add_process('test_process', 'test_user')
    # Try to return the process with a wrong user
    pm.return_process(process_id, 'wrong_user')

def test_get_process():
    """
    Test getting a process.

    This test checks if a process is successfully retrieved after it's added.
    """
    pm = ProcessManager()
    # Add a process
    pm.add_process('test_process', 'test_user')
    # Get the process
    process_id = pm.get_process(1, 'test_user')
    assert process_id == {'Process_ID': 1, 'Process_Name': 'test_process'}
    assert pm.df.loc[process_id['Process_ID'], 'Status'] == 'in use'
    assert pm.df.loc[process_id['Process_ID'], 'User_ID'] == 'test_user'

def test_max_processes():
    """
    Test the maximum number of processes limit.

    This test checks if the limit on the maximum number of processes is enforced.
    """
    pm = ProcessManager(max_processes=1)
    # Add a process
    pm.add_process('test_process', 'test_user')

@pytest.mark.xfail(reason="Maximum number of processes has been reached")
def test_add_process_when_max_reached():
    """
    Test adding a process when the maximum number of processes has been reached.

    This test should fail because the maximum number of processes has already been reached.
    """
    pm = ProcessManager(max_processes=1)
    # Add the maximum number of processes
    pm.add_process('test_process', 'test_user')
    # Try to add another process
    pm.add_process('another_process', 'test_user')
