import serial
import time

class PowerSupply:
    def __init__(self, port, vLim, cLim, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self._voltage = None
        self._current = None
        self.runCommand(f'SOVP{int(vLim)*100:04d}')
        self.runCommand(f'SOCP{int(cLim)*100:04d}')

    def runCommand(self, cmd, maxLength=25, doPrint=False) -> str:
        cmd = cmd.encode() + b'\r'
        sp = serial.Serial(self.port, self.baudrate,timeout=.2) # Open a serial connection
        sp.write(cmd) 
        response=b''
        i=0
        while(not(b'OK\r' in response)):
            response+= sp.read(size=1)
            if i>maxLength: break
        if doPrint: print(response)
        sp.close()
        assert (response[-3:] == b'OK\r'), 'no OK received'
        return response[:-3].decode('utf-8').replace('\r','')

    def ON(self): self.runCommand('SOUT1')
    
    def OFF(self): self.runCommand('SOUT0')

    def setVolt(self,volts, preset=3): self.runCommand(f'VOLT{preset:01d}{int(volts*100):04d}')

    def setCurr(self,curr, preset=3):
        self.runCommand(f'CURR{preset:01d}{int(curr*100):04d}')

    def setPreset(self,volt,curr, preset=3):
        self.runCommand(f'SETD{preset:01d}{int(volt*100):04d}{int(curr*100):04d}')

    def getPreset(self,preset=3) -> tuple:
        resp = self.runCommand(f'GETS{preset:01d}',12)
        assert (len(resp) == 8), f'Incorrent response length: {len(resp)}, {resp}'
        return float(resp[:4])/100 , float(resp[4:8])/100

    def enablePreset(self,preset=3): self.runCommand(f'SABC{preset:01d}',3)

    def currentPreset(self):
        response = self.runCommand('GABC',4)
        return int(response)

    def readValues(self) -> tuple:
        rpnse = self.runCommand('GETD',13)
        assert (len(rpnse) == 9), f'Incorrect response length: {len(rpnse)}, {rpnse}'
        return float(rpnse[:4])/100 , float(rpnse[4:8])/100, bool(rpnse[8])




def test():
    ps = PowerSupply('/dev/ttyUSB0')
    ps.ON()
    time.sleep(2)
    print(ps.readValues())
    ps.OFF()
    time.sleep(5)
    print(ps.readValues())

if __name__ == "__main__":
    test()
