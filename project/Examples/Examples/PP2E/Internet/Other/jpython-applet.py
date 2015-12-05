#######################################
# a simple java applet coded in Python
#######################################

from java.applet import Applet                            # get java superclass

class Hello(Applet):
    def paint(self, gc):                                  # on paint callback
        gc.drawString("Hello applet world", 20, 30)       # draw text message

if __name__ == '__main__':                                # if run stand-alone
    import pawt                                           # get java awt lib
    pawt.test(Hello())                                    # run under awt loop