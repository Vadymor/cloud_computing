import shutil

# create archive for http_triggered_function
shutil.make_archive('./archived_functions/http_triggered_function',
                    'zip',
                    './http_triggered_function')

# create archive for event_store_function
shutil.make_archive('./archived_functions/event_store_function',
                    'zip',
                    './event_store_function')
