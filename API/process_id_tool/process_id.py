import pandas as pd 
import threading

class ProcessManager():
    ''' 
    A class used to manage process IDs.

    ...

    Attributes
    ----------
    df : pandas.DataFrame
        a DataFrame to store process IDs, process names, and status
    max_processes : int
        the maximum number of processes that can be in use at one time

    Methods
    -------
    generate_process_id():
        Generates a unique process ID.
    add_process(process_name: str) -> int:
        Adds a process with the given name to the DataFrame and returns its ID.
    return_process(process_id: int):
        Returns a process with the given ID, making it available for reuse.
    get_process(process_name: str) -> int:
        Gets a process with the given name. If no available processes exist, adds a new process and returns its ID.
    '''
    def __init__(self, max_processes = 1000): 
        ''' 
        Constructs the attributes for the process manager object.

        Parameters
        ----------
            max_processes : int
                The maximum number of processes that can be in use at one time (default 1000)
        '''
        self.df = pd.DataFrame(columns=['Process_ID', 'Process_Name', 'Status', 'User_ID'])
        self.max_processes = max_processes
        self.lock = threading.RLock()


    def create_process_id(self):
        ''' 
        Generate a unique process ID.
        If the DataFrame is empty, start the IDs at 1. Otherwise, increment the highest existing ID.
        '''
        with self.lock:
            if self.df.empty:
                return 1
            else:
                return self.df['Process_ID'].max() + 1
        
        
    def add_process(self, process_name, user_id):
        ''' 
        Add a process.
        Generate a unique process ID, add a new row to the DataFrame with the process ID, process name, and status (set to 'in use'). 
        If there are already 1000 processes in use, raise an exception.
        '''
        with self.lock:
            if (self.df['Status'] == 'in use').sum() >= self.max_processes:
                raise Exception("Maximum number of processes in use")
            
            process_id = self.create_process_id()
            self.df.loc[process_id] = [process_id, process_name, 'in use', user_id]
            return process_id



    def return_process(self, process_id, user_id, process_name):
        """
        Return a process.
        Find the row in the DataFrame with the given process ID and process name and set its status to 'available'. 
        If the process ID does not exist in the DataFrame, if it's not in use, or if it's not associated with the user, or if the process name does not match, raise an exception.
        """
        with self.lock:
            if process_id not in self.df.index:
                raise Exception("Process ID not found")
            elif self.df.loc[process_id, 'Status'] != 'in use':
                raise Exception("Process ID was not in use")
            elif self.df.loc[process_id, 'User_ID'] != user_id:
                raise Exception("Process ID is not associated with this user")
            elif self.df.loc[process_id, 'Process_Name'] != process_name:
                raise Exception("Process name does not match")
            self.df.loc[process_id, 'Status'] = 'available'


    def get_process(self, process_id, user_id):
        """
        Get a process.
        Find the row in the DataFrame where the status is 'in use' and the user_id matches, and return the process ID and process name. 
        If no such process exists, raise an exception.
        """
        with self.lock:
            process_row = self.df[(self.df.index == process_id) & (self.df['User_ID'] == user_id) & (self.df['Status'] == 'in use')]
            if not process_row.empty:
                return {"Process_ID": process_id, "Process_Name": process_row.iloc[0]['Process_Name']}
            else:
                raise ValueError("Process does not exist")