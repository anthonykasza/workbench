
import zerorpc
import pprint

def main():

    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")

    results = c.batch_work_request('view_customer', {})
    pprint.pprint(results)

def test():
    ''' customer_report test '''
    main()

if __name__ == '__main__':
    main()

