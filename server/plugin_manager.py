
''' A simple plugin manager. Rolling my own for three reasons:
    1) Environmental scan did not give me quite what I wanted.
    2) The super simple examples didn't support automatic/dynamic loading.
    3) I kinda wanted to understand the process :)
'''

import os, sys, time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Local modules
try:
    from . import plugin_validator
except ValueError:
    import plugin_validator

class PluginManager(FileSystemEventHandler):

    def __init__(self, plugin_callback, plugin_dir = 'workers'):
        self.plugin_callback = plugin_callback
        self.plugin_validator = plugin_validator.PluginValidator()

        # First go through the existing python files in the plugin directory
        plugin_path = os.path.realpath(plugin_dir)
        sys.path.append(plugin_dir)
        for f in [os.path.join(plugin_dir, child) for child in os.listdir(plugin_dir)]:
            self.add_plugin(f)

        # Now setup dynamic monitoring of the plugins directory
        observer = Observer()
        observer.schedule(self, path=plugin_path)
        observer.start()

    def on_created(self, event):
        ''' Watcher callback '''
        self.add_plugin(event.src_path)
    def on_modified(self, event):
        ''' Watcher callback '''
        self.add_plugin(event.src_path)

    def add_plugin(self, f):
        ''' Adding and verifying plugin '''
        if f.endswith('.py'):
            plugin_path = f[:-3]
            plugin_name = os.path.basename(plugin_path)
            plugin = self.plugin_validator.validate(plugin_name)
            if plugin:
                mod_time = datetime.utcfromtimestamp(os.path.getmtime(f))
                self.plugin_callback(plugin, mod_time)


# Just create the class and run it for a test
def _test():

    # This is just a fake plugin callback for the test
    def new_plugin(plugin):
        print plugin

    # Create Plugin Manager
    plugins = PluginManager(new_plugin)

if __name__ == "__main__":
    _test()
