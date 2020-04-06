from P4 import P4

import time
import threading

# Threaded P4V Sync function
def p4_sync():
    global synced_files
    synced_files = p4.run( 'sync', '-f' )
    return synced_files

# Threaded P$v Sync callback
def p4_sync_callback( synced_files_from_p4 ):
    global files_synced
    synced_files = synced_files_from_p4
    files_synced = True

# 
threaded_callback_lock = threading.Lock()
class Threaded_Callback (threading.Thread):
    def __init__(self, thread_id, function, callback):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.function = function
        self.callback = callback
    
    def run(self):
        returnValue = self.function()

        threaded_callback_lock.acquire()
        self.callback( returnValue )
        threaded_callback_lock.release()

game_name = 'HaberDashers'
synced_files = {}
files_synced = False

if __name__ == '__main__':

    print( '----------------------------------------------------------------------------------------------------' )
    print( '{} - Step 1: Update the local workspcae for P4'.format( game_name ) )
    print( '----------------------------------------------------------------------------------------------------' )

    # Perforce Settings
    p4 = P4()
    p4.user = 'daily_builds'
    p4.password = 'gKv52w!*'
    p4.client = 'NightlyBuild_HaberDashers'

    # Connect to the perforce server
    success = p4.connect()
    print( success )

    p4_thread = Threaded_Callback(1, p4_sync, p4_sync_callback)
    p4_thread.start()
    
    start_time = time.time()
    while( not files_synced ):
        print( "Time Elapsed: {:.2f}".format( time.time() - start_time ), end='\r')

    print( 'Completed Perfoce Sync in {:.2f} seconds'.format( time.time() - start_time ) )

    files_updated = 0
    files_deleted = 0
    for file in synced_files:
        if file['action'] == 'refreshed':
            continue

        if file['action'] == 'deleted':
            files_deleted += 1
            continue

        files_updated += 1
        update_message = str(files_updated) + ": "

        relative_file_name = file['clientFile']
        name_loc = relative_file_name.find( game_name )
        relative_file_name = relative_file_name[ name_loc + len(game_name):]

        update_message += relative_file_name + " ( "
        update_message += file['rev'] + " ) - "
        update_message += file['action']

        print(update_message)

    if files_deleted > 0:
        print( '{} files marked for deleted in total'.format( files_deleted ) )
    if files_updated == 0:
        print( 'All files are current' )

    print( '{} - Step 1: Complete'.format( game_name ) )
    input( 'Press Enter to continue...')
