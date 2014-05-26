# -*- coding: utf-8 -*-
class si4703:
    ''' 
    Each sub-class in this file represents a register within the si4703 capable of being read.
    Not all registers are capable of being written to
    Some bits are capable of being written to, but should always be set to zero. Such registers have commented placeholders.
    '''
    import smbus

    i2c = smbus.SMBus(1)

    print "test2"
    def init(self):
        '''
        This is the initial setup for the Si4703. The encompasses setting up the GPIO pins on the Pi as the protocol for putting the Si4703 is 2-wire (read: "SMBus") mode
        The protocl is covered in the programming guide for the Si4703 dubbed "AN230"
        http://www.silabs.com/Support%20Documents/TechnicalDocs/AN230.pdf
        '''
        from time import sleep
        import RPi.GPIO as GPIO
        
        GPIO.setmode(GPIO.BCM)   ## We will use board numbering instead of pin numbering. 
        GPIO.setup(23 ,GPIO.OUT) ## RST
        GPIO.setup(0 ,GPIO.OUT)  ## SDA

        GPIO.output(0 ,GPIO.LOW) ## This block of code puts the Si4703 into 2-wire mode per instructions on page 7  of AN230
        sleep(.1)                        ## Actually, I'm not sure how this block of code works. According to the aforementioned page 7, it shouldn't
        GPIO.output(23 ,GPIO.LOW) ## But I ripped this code off somewhere else, so I'm not gonna bash it. Great work to the OP
        sleep(.1)
        GPIO.output(23 ,GPIO.HIGH)
        sleep(0.5)
        
        si4703.update_registry(self)
        si4703.TEST_1.POWER_SEQUENCE = True
        si4703.write_registry(self)
        si4703.TEST_1.POWER_SEQUENCE = False
        sleep(1)
        
        si4703.POWER_CONFIG.DMUTE = 1
        si4703.POWER_CONFIG.ENABLE = 1
        si4703.write_registry(self)
        sleep(1)

        si4703.SYS_CONFIG_2.VOLUME = 15
        si4703.write_registry(self)
        sleep(0.1)
      
        si4703.CHANNEL.CHAN = 85
        si4703.write_registry(self)
        sleep(0.1)
        si4703.CHANNEL.TUNE = 1
        si4703.write_registry(self)

        while si4703.STATUS_RSSI.STC == 0:
            sleep(0.1)
            si4703.update_registry(self)
        si4703.CHANNEL.TUNE = 0
        si4703.write_registry(self)

    # from the programmers guide: "ENABLE=1 turns the device on while DISABLE=1 turns the device off (powerdown mode)."
    def turn_off (self):
        from time import sleep
        si4703.POWER_CONFIG.DISABLE = 1
        si4703.write_registry(self)
        sleep(0.1)
        
    def convert_reg_readings (self, old_registry, reorder):
        '''
        (list, int) ->>> list
        When Python reads  the registry of the si4703 it places all 16 registers into a 32 item list (each item being a single byte). 
        This functioon gives each register its own item.
        The register at index 0 is 0x0A. If reorder is set to 1, then index 0 will be 0x00. 
        '''
        i = 0
        response = []
        while i <=31:
            first_byte = str(bin(old_registry[i]))
            second_byte = str(bin(old_registry[i+1]))
            
            first_byte = first_byte.replace("0b", "", 1)
            second_byte = second_byte.replace("0b", "", 1)

            while len(first_byte) < 8:
                first_byte = "0" + first_byte
            while len(second_byte) < 8:
                second_byte = "0" + second_byte
                
            full_register = first_byte + second_byte
            full_register = int(full_register, 2)
            
            response.append(full_register)
            i += 2
            
        if reorder == 1:
            response = si4703.reorder_reg_readings(self, response)

        return response

    def reorder_reg_readings (self, sixteen_item_list):
        '''
        Since the si4703 starts reading at register 0x0A and wraps back around at 0x0F, the data can be hard to understand.
        This re-orders the data such that the first itme in the list is 0x00, the second item is 0x01.....twelfth item is 0x0C
        '''
        original = sixteen_item_list
        response = []

        ##The item at index 6  is register 0x00
        response.append(original[6])    #0x00
        response.append(original[7])    #0x01
        response.append(original[8])    #0x02
        response.append(original[9])    #0x03
        response.append(original[10])   #0x04
        response.append(original[11])   #0x05
        response.append(original[12])   #0x06
        response.append(original[13])   #0x07
        response.append(original[14])   #0x08
        response.append(original[15])   #0x09
        response.append(original[0])    #0x0A
        response.append(original[1])    #0x0B
        response.append(original[2])    #0x0C
        response.append(original[3])    #0x0D
        response.append(original[4])    #0x0E
        response.append(original[5])    #0x0F

        return response
    def update_registry (self):
        '''
        This method reads all registers from the Si4703, and stores then into a 32 item array
        Then, it converts the 32 items into a 16-item array (1 item for each of the 16 registers)
        Since for some odd reason the Si4703 always starts reading at 0x0A, this method also reorders the last array such that its first item is 0x00
        Finally this method parses the data into local memory
        '''
        raw_data = []
        cmd = str(si4703.POWER_CONFIG.DSMUTE) + str(si4703.POWER_CONFIG.DMUTE) + str(si4703.POWER_CONFIG.MONO) + "0" + str(si4703.POWER_CONFIG.RDSM) + str(si4703.POWER_CONFIG.SKMODE) + str(si4703.POWER_CONFIG.SEEKUP) + str(si4703.POWER_CONFIG.SEEK)
        cmd = int(cmd, 2)
        try:
            raw_data = si4703.i2c.read_i2c_block_data(0x10,cmd,32)
        except:
            print "Exception in method 'update_registry' while trying to read from si4703"
        reordered_registry = si4703.convert_reg_readings(self, raw_data, 1)
        
        current_reg = [] 
        ## DEVICE_ID                    #0x00
        current_reg = reordered_registry[0]
        si4703.DEVICE_ID.PN = si4703.get_reg_value(self, current_reg, 0, 4)
        si4703.DEVICE_ID.MFGID = si4703.get_reg_value(self, current_reg, 4, 12)

        ## CHIP_ID                      #0x01
        current_reg = reordered_registry[1]
        si4703.CHIP_ID.REV = si4703.get_reg_value(self, current_reg, 0, 6)
        si4703.CHIP_ID.DEV = si4703.get_reg_value(self, current_reg, 6, 4)
        si4703.CHIP_ID.FIRMWARE = si4703.get_reg_value(self, current_reg, 10, 6)

        ## POWER_CONFIG                 #0x02
        current_reg = reordered_registry[2]
        si4703.POWER_CONFIG.DSMUTE = si4703.get_reg_value(self, current_reg, 0, 1)
        si4703.POWER_CONFIG.DMUTE = si4703.get_reg_value(self, current_reg, 1, 1)
        si4703.POWER_CONFIG.MONO = si4703.get_reg_value(self, current_reg, 2, 1)
        ##si4703.POWER_CONFIG.UNUSED = si4703.get_reg_value(self, current_reg, 3, 1)
        si4703.POWER_CONFIG.RDSM = si4703.get_reg_value(self, current_reg, 4, 1)
        si4703.POWER_CONFIG.SKMODE = si4703.get_reg_value(self, current_reg, 5, 1)
        si4703.POWER_CONFIG.SEEKUP = si4703.get_reg_value(self, current_reg, 6, 1)
        si4703.POWER_CONFIG.SEEK = si4703.get_reg_value(self, current_reg, 7, 1)
        ##si4703.POWER_CONFIG.UNUSED = si4703.get_reg_value(self, current_reg, 8, 1)
        si4703.POWER_CONFIG.DISABLE = si4703.get_reg_value(self, current_reg, 9, 1)
        ##si4703.POWER_CONFIG.UNUSED = si4703.get_reg_value(self, current_reg, 10, 1)
        ##si4703.POWER_CONFIG.UNUSED = si4703.get_reg_value(self, current_reg, 11, 1)
        ##si4703.POWER_CONFIG.UNUSED = si4703.get_reg_value(self, current_reg, 12, 1)
        ##si4703.POWER_CONFIG.UNUSED = si4703.get_reg_value(self, current_reg, 13, 1)
        ##si4703.POWER_CONFIG.UNUSED = si4703.get_reg_value(self, current_reg, 14, 1)
        si4703.POWER_CONFIG.ENABLE = si4703.get_reg_value(self, current_reg, 15, 1)

        ## CHANNEL                      #0x03
        current_reg = reordered_registry[3]
        si4703.CHANNEL.TUNE = si4703.get_reg_value(self, current_reg, 0, 1)
        ##si4703.CHANNEL.UNUSED = si4703.get_reg_value(self, current_reg, 1, 1)
        ##si4703.CHANNEL.UNUSED = si4703.get_reg_value(self, current_reg, 2, 1)
        ##si4703.CHANNEL.UNUSED = si4703.get_reg_value(self, current_reg, 3, 1)
        ##si4703.CHANNEL.UNUSED = si4703.get_reg_value(self, current_reg, 4, 1)
        ##si4703.CHANNEL.UNUSED = si4703.get_reg_value(self, current_reg, 5, 1)
        si4703.CHANNEL.CHAN = si4703.get_reg_value(self, current_reg, 6, 10)

        ## SYS_CONFIG_1                 0x04
        current_reg = reordered_registry[4]
        si4703.SYS_CONFIG_1.RDSIEN = si4703.get_reg_value(self, current_reg, 0, 1)
        si4703.SYS_CONFIG_1.STCIEN = si4703.get_reg_value(self, current_reg, 1, 1)
        ##si4703.SYS_CONFIG_1.UNUSED = si4703.get_reg_value(self, current_reg, 2, 1)
        si4703.SYS_CONFIG_1.RDS = si4703.get_reg_value(self, current_reg, 3, 1)
        si4703.SYS_CONFIG_1.DE = si4703.get_reg_value(self, current_reg, 4, 1)
        si4703.SYS_CONFIG_1.AGCD = si4703.get_reg_value(self, current_reg, 5, 1)
        ##si4703.SYS_CONFIG_1.UNUSED = si4703.get_reg_value(self, current_reg, 6, 1)
        ##si4703.SYS_CONFIG_1.UNUSED = si4703.get_reg_value(self, current_reg, 7, 1)
        si4703.SYS_CONFIG_1.BLNDADJ = si4703.get_reg_value(self, current_reg, 8, 2)
        si4703.SYS_CONFIG_1.GPIO3 = si4703.get_reg_value(self, current_reg, 10, 2)
        si4703.SYS_CONFIG_1.GPIO2 = si4703.get_reg_value(self, current_reg, 12, 2)
        si4703.SYS_CONFIG_1.GPIO1 = si4703.get_reg_value(self, current_reg, 14, 2)

        ## SYS_CONFIG_2                 0x05
        current_reg = reordered_registry[5]
        si4703.SYS_CONFIG_2.SEEKTH = si4703.get_reg_value(self, current_reg, 0, 8)
        si4703.SYS_CONFIG_2.BAND = si4703.get_reg_value(self, current_reg, 8, 2)
        si4703.SYS_CONFIG_2.SPACE = si4703.get_reg_value(self, current_reg, 10, 2)
        si4703.SYS_CONFIG_2.VOLUME = si4703.get_reg_value(self, current_reg, 12, 4)

        ## SYS_CONFIG_3                 0x06
        current_reg = reordered_registry[6]
        si4703.SYS_CONFIG_3.SMUTER = si4703.get_reg_value(self, current_reg, 0, 2)
        si4703.SYS_CONFIG_3.SMUTEA = si4703.get_reg_value(self, current_reg, 2, 2)
        ##si4703.SYS_CONFIG_3.UNUSED = si4703.get_reg_value(self, current_reg, 4, 1)
        ##si4703.SYS_CONFIG_3.UNUSED = si4703.get_reg_value(self, current_reg, 5, 1)
        ##si4703.SYS_CONFIG_3.UNUSED = si4703.get_reg_value(self, current_reg, 6, 1)
        si4703.SYS_CONFIG_3.VOLEXT = si4703.get_reg_value(self, current_reg, 7, 1)
        si4703.SYS_CONFIG_3.SKSNR = si4703.get_reg_value(self, current_reg, 8, 4)
        si4703.SYS_CONFIG_3.SKCNT = si4703.get_reg_value(self, current_reg, 12, 4)

        ## TEST_1                       0x07
        current_reg = reordered_registry[7]
        si4703.TEST_1.XOSCEN = si4703.get_reg_value(self, current_reg, 0, 1)
        si4703.TEST_1.AHIZEN = si4703.get_reg_value(self, current_reg, 1, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 2, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 3, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 4, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 5, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 6, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 7, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 8, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 9, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 10, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 11, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 12, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 13, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 14, 1)
        ##si4703.TEST_1.UNUSED = si4703.get_reg_value(self, current_reg, 15, 1)

        ## TEST_2                       0x08        ALL BITS UNUSED
        current_reg = reordered_registry[8]
        ##si4703.TEST_2.UNUSED = si4703.get_reg_value(self, current_reg, 0, 16)

        ## BOOT_CONFIG                  0x09        ALL BITS UNUSED
        current_reg = reordered_registry[9]
        ##si4703.BOOT_CONFIG.UNUSED = si4703.get_reg_value(self, current_reg, 0, 16)

        ## STATUS_RSSI                  0x0A
        current_reg = reordered_registry[10]
        si4703.STATUS_RSSI.RDSR = si4703.get_reg_value(self, current_reg, 0, 1)
        si4703.STATUS_RSSI.STC = si4703.get_reg_value(self, current_reg, 1, 1)
        si4703.STATUS_RSSI.SFBL = si4703.get_reg_value(self, current_reg, 2, 1)
        si4703.STATUS_RSSI.AFCRL = si4703.get_reg_value(self, current_reg, 3, 1)
        si4703.STATUS_RSSI.RDSS = si4703.get_reg_value(self, current_reg, 4, 1)
        si4703.STATUS_RSSI.BLER_A = si4703.get_reg_value(self, current_reg, 5, 2)
        si4703.STATUS_RSSI.ST = si4703.get_reg_value(self, current_reg, 7, 1)
        si4703.STATUS_RSSI.RSS = si4703.get_reg_value(self, current_reg, 8, 8)

        ## READ_CHAN                    0x0B
        current_reg = reordered_registry[11]
        si4703.READ_CHAN.BLER_B = si4703.get_reg_value(self, current_reg, 0, 2)
        si4703.READ_CHAN.BLER_C = si4703.get_reg_value(self, current_reg, 2, 2)
        si4703.READ_CHAN.BLER_D = si4703.get_reg_value(self, current_reg, 4, 2)
        si4703.READ_CHAN.READ_CHAN = si4703.get_reg_value(self, current_reg, 6, 10)

        ## RDS_A                        0x0C
        current_reg = reordered_registry[12]
        si4703.RDS_A.RDS_A = si4703.get_reg_value(self, current_reg, 0, 16)

        ## RDS_B                        0x0D
        current_reg = reordered_registry[13]
        si4703.RDS_B.RDS_B = si4703.get_reg_value(self, current_reg, 0, 16)

        ## RDS_C                        0x0E
        current_reg = reordered_registry[14]
        si4703.RDS_C.RDS_C = si4703.get_reg_value(self, current_reg, 0, 16)

        ## RDS_D                        0x0F
        current_reg = reordered_registry[15]
        si4703.RDS_D.RDS_D = si4703.get_reg_value(self, current_reg, 0, 16)


    def get_reg_value(self, register, begin, length):
        '''
        This class continually has to copy the contents of the Si4703's registers to the Pi's internal memory. This function helps parse the data from the Si4703.
        In order to parse the data, we need the raw data, along with the location of a property and its length in bits (ie READCHAN's location would be index 6 and its length would be 9 bits)

        Internally, Python converts any hex, octal, or binary number into an integer for storage. This is why the register is represented as an integer at first. We then convert it to a string of nothing but 1s and 0s, and add extra zeros until it is 16 bits long.
        After doing this, we can use the location and length information to return the value of a property.
        '''
        int_register = register                        ##give this a friendlier name
        str_register = str(bin(int_register))          ##Convert the register to a string (ie 15 becomes "0b1111") 
        str_register = str_register.replace("0b", "")  ##Get rid of the "0b" prefix (ie 15 would now become "1111") 
        while len(str_register) < 16:                  ##We want the output to be 16 bits long 
            str_register = "0" + str_register          ##Add preceeding zeros until it IS 16 characters long
        response = str_register[begin : begin + length]##Weed out all the bits we don't need
        response = int(response, 2)                    ##Convert it back to an assignable integer
        
        return response

    def write_registry(self):
        '''
        Refreshes the registers on the device with the ones stored in local memory on the Pi.
        It will only refresh the registers 0x02-07, as all other registers cannot be written to
        '''
        main_list = []
        crazy_first_number = 0
        
        first_byte = 0
        second_byte = 0

        ## POWER_CONFIG                 #0x02
        first_byte = str(si4703.POWER_CONFIG.DSMUTE) + str(si4703.POWER_CONFIG.DMUTE) + str(si4703.POWER_CONFIG.MONO) + "0" + str(si4703.POWER_CONFIG.RDSM) + str(si4703.POWER_CONFIG.SKMODE) + str(si4703.POWER_CONFIG.SEEKUP) + str(si4703.POWER_CONFIG.SEEK)
        second_byte = "0" + str(si4703.POWER_CONFIG.DISABLE) + "00000" + str(si4703.POWER_CONFIG.ENABLE)
        first_byte = int(first_byte, 2)
        crazy_first_number = first_byte
        second_byte = int(second_byte, 2)
        main_list.append(second_byte)

        ## CHANNEL                      #0x03
        first_byte = str(si4703.CHANNEL.TUNE) + "0000000"
        second_byte =si4703.return_with_padding(self, si4703.CHANNEL.CHAN, 10)
        first_byte = int(first_byte, 2)
        second_byte = int(second_byte, 2)
        main_list.append(first_byte)
        main_list.append(second_byte)

        ## SYS_CONFIG_1                 0x04
        first_byte = str(si4703.SYS_CONFIG_1.RDSIEN) + str(si4703.SYS_CONFIG_1.STCIEN) + "0" + str(si4703.SYS_CONFIG_1.RDS) + str(si4703.SYS_CONFIG_1.DE) + str(si4703.SYS_CONFIG_1.AGCD) + "00"
        second_byte = si4703.return_with_padding(self, si4703.SYS_CONFIG_1.BLNDADJ, 2) + si4703.return_with_padding(self, si4703.SYS_CONFIG_1.GPIO3, 2) + si4703.return_with_padding(self, si4703.SYS_CONFIG_1.GPIO2, 2) + si4703.return_with_padding(self, si4703.SYS_CONFIG_1.GPIO1, 2)
        first_byte = int(first_byte, 2)
        second_byte = int(second_byte, 2)
        main_list.append(first_byte)
        main_list.append(second_byte)

        ## SYS_CONFIG_2                 0x05
        first_byte = si4703.return_with_padding(self, si4703.SYS_CONFIG_2.SEEKTH, 8)
        second_byte = si4703.return_with_padding(self, si4703.SYS_CONFIG_2.BAND, 2) + si4703.return_with_padding(self, si4703.SYS_CONFIG_2.SPACE, 2) + si4703.return_with_padding(self, si4703.SYS_CONFIG_2.VOLUME, 4)
        first_byte = int(first_byte, 2)
        second_byte = int(second_byte, 2)
        main_list.append(first_byte)
        main_list.append(second_byte)

        ## SYS_CONFIG_3                 0x06
        first_byte = si4703.return_with_padding(self, si4703.SYS_CONFIG_3.SMUTER, 2) + si4703.return_with_padding(self, si4703.SYS_CONFIG_3.SMUTEA, 2) + "000" + str(si4703.SYS_CONFIG_3.VOLEXT)
        second_byte = si4703.return_with_padding(self, si4703.SYS_CONFIG_3.SKSNR, 4) + si4703.return_with_padding(self, si4703.SYS_CONFIG_3.SKCNT, 4)
        first_byte = int(first_byte, 2)
        second_byte = int(second_byte, 2)
        main_list.append(first_byte)
        main_list.append(second_byte)
        
        ## TEST_1                       0x07
        if si4703.TEST_1.POWER_SEQUENCE == 55:   ##Since all but the first two bits in this register are unused, and we only write to this to power up/down the device, it seems unessary to write this registry every time. Especially considering that writing 0 to the remaining register while in operation can prove fatal
            first_byte = str(si4703.TEST_1.XOSCEN) + str(si4703.TEST_1.AHIZEN) + si4703.return_with_padding(self, si4703.TEST_1.RESERVED_FIRST_BYTE, 4)
            second_byte = si4703.return_with_padding(self, si4703.TEST_1.RESERVED_SECOND_BYTE, 8)
            first_byte = int(first_byte, 2)
            second_byte = int(second_byte, 2)
            main_list.append(first_byte)
            main_list.append(second_byte)
        if si4703.TEST_1.POWER_SEQUENCE == True:##debug code for TEST_1. remove after debugging
            main_list.append(129) 

        print main_list
        print crazy_first_number
        w6 = si4703.i2c.write_i2c_block_data(0x10, crazy_first_number, main_list)
        si4703.update_registry(self)

    def return_with_padding (self, item_as_integer, length):
        item_as_integer = str(bin(item_as_integer))
        item_as_integer = item_as_integer.replace("0b", "")

        while len(item_as_integer) < length:
            item_as_integer = "0" + item_as_integer

        return item_as_integer
    def tune (self, frequency):
        '''
        Frequency (Mhz) (ie 98.5 tunes to 98.5; 104.5 tunes to 104.5)
        The si4703 doesn't use verbatim tuning. Such that you cannot tune to 104.5 by setting CHAN to 1045.
        Instead, setting CHAN to 0 will tune to the lowest frequency allowable for your region. Your region is set by setting BAND.
        Setting CHAN to 1 will tune to the lowest frequency allowable + spacing
        ie
        BAND = 0        ## 87.5-108.0 (default)
        SPACE = 0       ## 200 Khz (default)
        CHAN = 1
        The tuned frequency would be 87.7
        '''
        from time import sleep, time
        
        frequency = float(frequency)
        channel = 0
        spacing = 0

        if si4703.SYS_CONFIG_2.SPACE == 0:  # Typical spacing for USA & Australia (default) - 200 Khz or 0.2 Mhz
            spacing = 20
        elif si4703.SYS_CONFIG_2.SPACE == 1:# Typical spacing for Europe & Japan            - 100 Khz or 0.1 Mhz
            spacing = 10
        elif si4703.SYS_CONFIG_2.SPACE == 3:# Minimum spacing allowed                       -  50 Khz or 0.05 Mhz
            spacing = 5
            
        if si4703.SYS_CONFIG_2.BAND == 0:   # 87.5-108.0 Mhz for USA/Europe
            channel = ((frequency*100)-8750)/spacing
        else:                               # 76.0-108.0 Mhz(Japan wide-band) or 76.0-90.0 Mhz (Japan)
            channel = ((frequency*100)-7600)/spacing # These fall into the same if statement because the begining of the bands both start at 76.0 Mhz

        channel = int(channel)              #We turned this into a float earlier for some proper division, so we better turn it back to an int before we try to write it

        si4703.CHANNEL.TUNE = 1             #Must set the TUNE bit in order to perform a tune 
        si4703.CHANNEL.CHAN = channel       #Also, we need to tell it what to tune to
        si4703.write_registry(self)         #Now write all of this to the si4703

        si4703.wait_for_tune(self)
            
        si4703.CHANNEL.TUNE = 0             #In order to do anything else, we have to clear the TUNE bit once the device successfully (or unsuccessfully for that matter) tuned
        si4703.write_registry(self)

    def wait_for_tune (self):
        from time import sleep, time
        
        begining_time = time()
        
        while si4703.STATUS_RSSI.ST == 0:   #The si4703 sets the ST bit high whenever it is finished tuning/seeking
            if time() - begining_time > 0.9:  #If we've been in this loop for more than two seconds, then get out
                break
            sleep(0.1)                      #This is only precautionary. We don't want to overload anything by reading/writing over and over and back to back
            si4703.update_registry(self)

    def seek_right (self):
        '''
        Seeks to the closest station above the currently tuned station.
        '''
        si4703.update_registry(self)
        
        si4703.POWER_CONFIG.SEEKUP = 1
        si4703.POWER_CONFIG.SEEK = 1
        si4703.write_registry(self)

        si4703.wait_for_tune(self)

        si4703.POWER_CONFIG.SEEK = 0
        si4703.write_registry(self)
    def seek_left (self):
        '''
        Seeks to the closest station below the currently tuned station.
        '''
        si4703.update_registry(self)
        
        si4703.POWER_CONFIG.SEEKUP = 0
        si4703.POWER_CONFIG.SEEK = 1
        si4703.write_registry(self)

        si4703.wait_for_tune(self)

        si4703.POWER_CONFIG.SEEK = 0
        si4703.write_registry(self)

    def get_channel (self):
        '''
        get_channel() ->> float
        Returns the frequency currenly tuned to
        Since the CHAN property is only a valid property after a tune operation and not a seek operation, we must use the READ_CHAN property to get the frequency
        Also, just like CHAN, the frequency isn't verbatim and is encoded somewhat such that if READ_CHAN = 0 then the frequency is the lowest possible frequency for the reciever
        '''
        channel = si4703.READ_CHAN.READ_CHAN
        spacing = 0
        frequency = 0.0

        if si4703.SYS_CONFIG_2.SPACE == 0:  # Typical spacing for USA & Australia (default) - 200 Khz or 0.2 Mhz
            spacing = 20
        elif si4703.SYS_CONFIG_2.SPACE == 1:# Typical spacing for Europe & Japan            - 100 Khz or 0.1 Mhz
            spacing = 10
        elif si4703.SYS_CONFIG_2.SPACE == 3:# Minimum spacing allowed                       -  50 Khz or 0.05 Mhz
            spacing = 5
            
        if si4703.SYS_CONFIG_2.BAND == 0:   # 87.5-108.0 Mhz for USA/Europe
            frequency = (((channel * spacing) + 8750) / 100.0)
        else:                               # 76.0-108.0 Mhz(Japan wide-band) or 76.0-90.0 Mhz (Japan)
            frequency = (((channel * spacing) + 8750) / 100.0)# These fall into the same if statement because the begining of the bands both start at 76.0 Mhz
        return frequency

    def toggle_mute (self):
        '''
        Toggles the mute feature. The si4703 is muted by default once the device is enabled.
        Changing the mute feature is done by chaning the Disable Mute property (DMUTE)
        '''
        if si4703.POWER_CONFIG.DMUTE == 0:  
            si4703.POWER_CONFIG.DMUTE = 1
        else:
            si4703.POWER_CONFIG.DMUTE = 0
        
        si4703.write_registry(self)

    #
    # volume must be between 0 and 15 (0 is mute)
    #
    def volume (self, volume):
        '''
        Int must be a integer no lower than 0 and no higher than 15
        '''
        if 0 <= volume <= 15:   ## Did the user provide a proper value between 0 and 15?
            pass
        elif volume < 0:        ## Well at this point they didn't give us a good volume integer, so we're going to mute it if it's too low
            volume = 0
        else:                   ## And in the last case, where it is too high, we'll set it to the highest possible setting
            volume = 15
            
        #si4703.SYS_CONFIG_2.VOLUME = int ## Finally, let's save all that work
        si4703.SYS_CONFIG_2.VOLUME = volume ## Finally, let's save all that work
        si4703.write_registry(self)      ## And then write it in stone

    def tune_left (self):
        '''
        Analogous to a tuning dial, this tunes to the next available frequency on the left of the current station. 
        '''
        current_channel = si4703.get_channel(self)
        if si4703.SYS_CONFIG_2.SPACE == 0:
            current_channel -= 0.2
        elif si4703.SYS_CONFIG_2 == 1:
            current_channel -= 0.1
        else:
            current_channel -= 0.05

        si4703.tune(self, current_channel)
    def tune_right (self):
        '''
        Analogous to a tuning dial, this tunes to the next available frequency on the right of the current station. 
        '''
        current_channel = si4703.get_channel(self)
        if si4703.SYS_CONFIG_2.SPACE == 0:
            current_channel += 0.2
        elif si4703.SYS_CONFIG_2 == 1:
            current_channel += 0.1
        else:
            current_channel += 0.05

        si4703.tune(self, current_channel)
    def print_registry(self):
        print"POWER_CONFIG:"
        print"\t", "DSMUTE:", si4703.POWER_CONFIG.DSMUTE
        print"\t", "DMUTE:", si4703.POWER_CONFIG.DMUTE
        print"\t", "MONO:", si4703.POWER_CONFIG.MONO
        print"\t", "RDSM:", si4703.POWER_CONFIG.RDSM
        print"\t", "SKMODE:", si4703.POWER_CONFIG.SKMODE
        print"\t", "SEEKUP:", si4703.POWER_CONFIG.SEEKUP
        print"\t", "SEEK:", si4703.POWER_CONFIG.SEEK
        print"\t", "DISABLE:", si4703.POWER_CONFIG.DISABLE
        print"\t", "ENABLE:", si4703.POWER_CONFIG.ENABLE
        
        print"CHANNEL:"
        print"\t", "TUNE:", si4703.CHANNEL.TUNE 
        fmchan = si4703.CHANNEL.CHAN
        fmchan = (((fmchan*20)+8750)/10)
        print"\t", "CHAN:", si4703.CHANNEL.CHAN, "(", fmchan, ")"
        
        print"SYS_CONFIG_1:"
        print"\t", "RDSIEN:", si4703.SYS_CONFIG_1.RDSIEN
        print"\t", "STCIEN:", si4703.SYS_CONFIG_1.STCIEN
        print"\t", "RDS:", si4703.SYS_CONFIG_1.RDS
        print"\t", "DE:", si4703.SYS_CONFIG_1.DE
        print"\t", "AGCD:", si4703.SYS_CONFIG_1.AGCD
        print"\t", "BLNDADJ:", si4703.SYS_CONFIG_1.BLNDADJ
        print"\t", "GPIO3:", si4703.SYS_CONFIG_1.GPIO3
        print"\t", "GPIO2:", si4703.SYS_CONFIG_1.GPIO2
        print"\t", "GPIO1:", si4703.SYS_CONFIG_1.GPIO1
        
        print"SYS_CONFIG_2"
        print"\t", "SEEKTH:", si4703.SYS_CONFIG_2.SEEKTH
        print"\t", "BAND:", si4703.SYS_CONFIG_2.BAND
        print"\t", "SPACE:", si4703.SYS_CONFIG_2.SPACE
        print"\t", "VOLUME:", si4703.SYS_CONFIG_2.VOLUME
        
        print"SYS_CONFIG_3"
        print"\t", "SMUTER:", si4703.SYS_CONFIG_3.SMUTER
        print"\t", "SMUTEA:", si4703.SYS_CONFIG_3.SMUTEA
        print"\t","VOLEXT:", si4703.SYS_CONFIG_3.VOLEXT
        print"\t", "SKSNR:", si4703.SYS_CONFIG_3.SKSNR
        print"\t", "SKCNT:", si4703.SYS_CONFIG_3.SKCNT
        print"TEST_1"
        print"\t", "XOSCEN:", si4703.TEST_1.XOSCEN
        print"\t", "AHIZEN:", si4703.TEST_1.AHIZEN
        print"\t", "RESERVED_FIRST_BYTE:", si4703.TEST_1.RESERVED_FIRST_BYTE
        print"\t", "RESERVED_SECOND_BYTE:", si4703.TEST_1.RESERVED_SECOND_BYTE
      
    class DEVICE_ID:                    #0x00
        PN     = 0
        MFGID  = 0
    class CHIP_ID:                      #0x01
        REV    = 0
        DEV    = 0
        FIRMWARE=0
    class POWER_CONFIG:                 #0x02
        DSMUTE = 0
        DMUTE  = 0
        MONO   = 0
        ##     = 0
        RDSM   = 0
        SKMODE = 0
        SEEKUP = 0
        SEEK   = 0
        ##     = 0
        DISABLE= 0
        ##     = 0
        ##     = 0
        ##     = 0
        ##     = 0
        ##     = 0
        ENABLE = 0
        def FULL_REGISTER (self):  
            first_byte = str(DSMUTE) + str(DMUTE) + str(MONO) + "0" + str(RDSM) + str(SKMODE) + str(SEEKUP) + str(SEEK)
            first_byte = int(first_byte, 2)
            
            second_byte = "0" + str(DISABLE) + "00000" + str(ENABLE)
            second_byte = int(second_byte, 2)
            return [first_byte, second_byte]

    class CHANNEL:                      #0x03
        TUNE   = 0
        ##     = 0
        ##     = 0
        ##     = 0
        ##     = 0
        ##     = 0
        CHAN   = 0
    class SYS_CONFIG_1:                 #0x04
        RDSIEN = 0
        STCIEN = 0
        ##     = 0
        RDS    = 0
        DE     = 0
        AGCD   = 0
        ##     = 0
        ##     = 0
        BLNDADJ= 0
        GPIO3  = 0
        GPIO2  = 0
        GPIO1  = 0
    class SYS_CONFIG_2:                 #0x05
        SEEKTH = 0
        BAND   = 0
        SPACE  = 0
        VOLUME = 0
    class SYS_CONFIG_3:                 #0x06
        SMUTER = 0
        SMUTEA = 0
        ##     =
        ##     =
        ##     = 0
        VOLEXT = 0
        SKSNR  = 0
        SKCNT  = 0
    class TEST_1:                       #0x07
        XOSCEN = 0
        AHIZEN = 0
        RESERVED_FIRST_BYTE = 0 ## These bits are reserved, but their reset values are known, so they must be set-able 
        RESERVED_SECOND_BYTE = 0
        POWER_SEQUENCE = False
    class TEST_2:                       #0x08
        TEST_2 = 0
        ##ALL BITS IN THIS REGISTER ARE UNUSED
    class BOOT_CONFIG:                  #0x09
        BOOT_CONFIG = 0
        ##ALL BITS IN THIS REGISTER ARE UNUSED
    class STATUS_RSSI:                  #0x0A
        RDSR   = 0
        STC    = 0
        SFBL   = 0
        AFCRL  = 0
        RDSS   = 0
        BLER_A = 0
        ST     = 0
        RSSI   = 0
    class READ_CHAN:                    #0x0B
        BLER_B = 0 ##SEE THE STATUS_RSI REGISTER ABOVER FOR BLER-A
        BLER_C = 0
        BLER_D = 0
        READ_CHAN = 0
    class RDS_A:                        #0x0C
        RDS_A  = 0
    class RDS_B:                        #0x0D
        RDS_B  = 0
    class RDS_C:                        #0x0E
        RDS_C  = 0
    class RDS_D:                        #0x0F
        RDS_D  = 0

