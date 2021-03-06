
''' A simple plugin manager. Rolling my own for three reasons:
    1) Environmental scan did not give me quite what I wanted.
    2) The super simple examples didn't support automatic/dynamic loading.
    3) I kinda wanted to understand the process :)
'''

import os, sys
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import inspect

class PluginManager(FileSystemEventHandler):

    def __init__(self, plugin_callback, plugin_dir = 'workers'):

        # Set the callback
        self.plugin_callback = plugin_callback

        # First go through the existing python files in the plugin directory
        self.plugin_path = os.path.realpath(plugin_dir)
        sys.path.append(plugin_dir)
        for f in [os.path.join(plugin_dir, child) for child in os.listdir(plugin_dir)]:
            self.add_plugin(f)

        # Now setup dynamic monitoring of the plugins directory
        observer = Observer()
        observer.schedule(self, path=self.plugin_path)
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

            # Just the basename without extension
            plugin_name = os.path.splitext(os.path.basename(f))[0]

            # It's possible the plugin has been modified and needs to be reloaded
            if plugin_name in sys.modules:
                try:
                    handler = reload(sys.modules[plugin_name])
                except ImportError, error:
                    print 'Failed to import plugin: %s (%s)' % (plugin_name, error)
                    return
            else:
                # Not already loaded so try to import it
                try:
                    handler = __import__(plugin_name, globals(), locals(), [], -1)
                except ImportError, error:
                    print 'Failed to import plugin: %s (%s)' % (plugin_name, error)
                    return

            # Run the handler through plugin validation
            plugin = self.validate(handler)
            if plugin:

                # Okay must be successfully loaded so capture the plugin meta-data,
                # modification time and register the plugin through the callback
                plugin_info = {}
                plugin_info['class'] = plugin
                plugin_info['name'] = plugin_name
                plugin_info['dependencies'] = plugin.dependencies
                mod_time = datetime.utcfromtimestamp(os.path.getmtime(f))
                self.plugin_callback(plugin_info, mod_time)

    def run_test(self, handler):
        previousDir = os.getcwd()
        os.chdir(self.plugin_path)
        try:
            handler.test()
            return True
        except AttributeError:
            print 'Failure for plugin: %s' % (handler.__name__)
            print 'The file must have a top level test() method that runs'
            return False
        finally:
            os.chdir(previousDir)

    def validate(self, handler):
        ''' Validate the plugin, each plugin must have the following:
            1) The worker class must have an execute method: execute(self, input_data)
            2) The worker class must have a dependencies list (even if it's empty)
            3) The file must have a top level test() method
        '''

        # Check for the test method first
        methods = [name for name,value in inspect.getmembers(handler, callable)]
        if 'test' not in methods:
            print 'Failure for plugin: %s' % (handler.__name__)
            print 'Validation Error: The file must have a top level test() method'
            return None

        # Here we iterate through the classes found in the module and pick
        # the first one that satisfies the validation
        for name, plugin_class in inspect.getmembers(handler, inspect.isclass):
            if self.plugin_class_validation(plugin_class):
                return plugin_class

        # If we're here the plugin didn't pass validation
        print 'Failure for plugin: %s' % (handler.__name__)
        print 'Validation Error: Worker class is required to have a dependencies list and an execute method'

    def plugin_class_validation(self, plugin_class):

        # Every workbench plugin must have a dependencies list (even if it's empty)
        # Every workbench plugin must have an execute method.
        try:
            getattr(plugin_class, 'dependencies')
            getattr(plugin_class, 'execute')
        except AttributeError, error:
            return False

        return True


# Just create the class and run it for a test
def test():

    # This test actually does more than it appears. The workers
    # directory will get scanned and stuff will get loaded, etc.
    def new_plugin(plugin, mod_time):
        pass

    # Create Plugin Manager
    plugins = PluginManager(new_plugin)

if __name__ == "__main__":
    test()
