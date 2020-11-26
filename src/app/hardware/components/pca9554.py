################################################################################
# Author			: Ronald Dehuysser
# Creation date 	: 25.11.2020
# Langage			: microPython
# Filename			: pca9554.py
# Target		 	: M5Stack
# Description		: PCA9554A GPIO Expander
################################################################################

import time


#"""
#Pca9554 (8 bit I2C expander)
#"""
class PCA9554Relay():
    Pca9554_IN_REG = const(0x00) #Input register
    Pca9554_OUT_REG = const(0x01) #Output register
    Pca9554_POL_REG = const(0x02) #Polarity inversion register (1=data inverted)
    Pca9554_DIR_REG = const(0x03) #Config register (0=output, 1=input)
    Pca9554_I2CADDR = const(0x20)
    line=0xFF

    def __init__(self, i2c, line=0x00):
        self._i2c = i2c
        self.line=line
        self._setoutput()
        time.sleep(0.01)

    def off(self):
        #"""set output bit at 1"""
        currentValue = self._readOutByte()
        self._writeOutByte(bytearray([currentValue[0] | 1<<self.line]))

    def on(self):
        #"""reset output bit at 0"""
        currentValue = self._readOutByte()
        self._writeOutByte(bytearray([currentValue[0] & (255-(1<<self.line))]))

    def toggle(self):
        if self.isOn():
            self.off()
        else:
            self.on()

    def isOn(self):
        #"""read input bit value"""
        linevalue = self._readOutByte()
        ret = ((linevalue[0] >> self.line) & 1 )
        return ret == 0

    def isOff(self):
        return not self.isOn()

    def _readOutByte(self):
        #"""read input bit value"""
        return self._i2c.readfrom_mem(Pca9554_I2CADDR, Pca9554_OUT_REG, 1)

    def _writeOutByte(self,value):
        #"""write output byte value"""
        self._i2c.writeto_mem(Pca9554_I2CADDR, Pca9554_OUT_REG, value)

    def _setoutput(self):
        #"""set bit as output"""
        currentValue = self._i2c.readfrom_mem(Pca9554_I2CADDR , Pca9554_DIR_REG, 1)
        newValue = currentValue[0] & 255-(1<<self.line)
        self._i2c.writeto_mem(Pca9554_I2CADDR, Pca9554_DIR_REG, bytearray([newValue]))
