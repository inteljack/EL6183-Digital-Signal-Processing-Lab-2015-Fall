import pythonExPC, ilu, time, sys, string

def do_work(m, id, period):
    while 1:
        time.sleep(period)                        # every N seconds
        m.fromProducer(id, str(time.time()))      # to consumer process...

def main(argv):
    producer_id = argv[1]
    period      = string.atoi(argv[2])
    consumer    = ilu.ObjectOfSBH(pythonExPC.consumer, argv[3])
    do_work(consumer, producer_id, period)

if len(sys.argv) < 4:
    print "Usage: python producer.py ",
    print "PRODUCER-ID PERIOD-IN-SECONDS CONSUMER-SBH &"
    sys.exit(1)
else:
    main(sys.argv)
