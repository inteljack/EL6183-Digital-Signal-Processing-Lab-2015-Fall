import pythonExPC__skel, os, ilu

class realConsumer(pythonExPC__skel.consumer):
    def fromProducer(self, producerID, something):
        print 'producer', producerID, 'says: ', something

def main():
    # make a consumer object for producer processes to report to
    m = realConsumer()
    sbh = m.IluSBH()

    # fork off producer processes
    os.system("python producer.py producer1 7  '" + sbh + "'&");
    os.system("python producer.py producer2 10 '" + sbh + "'&");
    os.system("python producer.py producer3 23 '" + sbh + "'&");

    # now sit back in the ILU loop and wait for reports
    ilu.RunMainLoop()

main()
