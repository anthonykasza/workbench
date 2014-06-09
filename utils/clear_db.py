
''' This connects to the workbench server and tells it to clear the database..whee...'''
import zerorpc

if __name__ == "__main__":
    ''' This connects to the workbench server and tells it to clear the database..whee...'''

    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    c.clear_db()
    print 'Database completely wiped... Whee!'
