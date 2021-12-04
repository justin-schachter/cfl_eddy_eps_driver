###############################################################################
# Author: Justin Schachter (jschach@umich.edu)
###############################################################################
from ads7828 import ADS7828
from enum import IntEnum, Enum
from tabulate import tabulate

###########################################################################
# Main Class
###########################################################################
class EddyEps():
    
    ###########################################################################
    # MEMBER VARIABLES
    ###########################################################################
    _rev = None
    _i2c_bus_num = None
    _adc_0 = None
    _adc_1 = None
    _channels_per_adc = 8

    ###########################################################################
    # CONSTRUCTOR
    ###########################################################################
    def __init__(self, smbus_num=1):
        """
        """
        self.rev = 'REV A'
        self._i2c_bus_num = smbus_num
        
        #setup ADCs
        self._adc_0 = ADS7828(address=0x48, smbus_num=smbus_num)
        self._adc_1 = ADS7828(address=0x49, smbus_num=smbus_num)



    ###########################################################################
    # MEMBER CLASSES
    ###########################################################################
    class ChannelsRevA(IntEnum):
        """
        Global scope ADC channel name/value assignment
        on Eddy (i.e. ADC_XX on output regulation schematic)
        """
        LM_20_3V3_REG = 7
        LM_20_5V0_REG = 4 
        
        V_VBATT_RAW = 5
        I_VBATT_RAW = 6

        V_3V3 = 3
        I_3V3 = 2

        V_5V0 = 1
        I_5V0 = 0

        V_VBATT = 13
        I_VBATT = 14

    class AdcChannelScope(Enum):
        """
        Max value of global scope ADC channels on Eddy 
        (i.e. ADC_XX on output regulation schematic)
        """
        ADC_0 = range(0,8)  #ADC_0 to ADC_7
        ADC_1 = range(8,16) #ADC_8 to ADC_15

    
    ###########################################################################
    # PUBLIC MEMBER METHODS (PUBLIC API)
    ###########################################################################


    ###########################################################################
    # PRIVATE MEMBER METHODS
    ###########################################################################
    def _adc_read_channel_single_ended(self,adc,adc_ch):
        if ch < 0 or ch > self._channels_per_adc:
            raise ValueError('Invalid ch value provided')
        if adc == 'ADC_0' or adc == 0:
            return self._adc_0.read_channel_single_ended(adc_ch, internal_ref_on=True, ad_on=True)
        elif adc == 'ADC_1' or adc == 1:
            return self._adc_0.read_channel_single_ended(adc_ch, internal_ref_on=True, ad_on=True)
        else:
            raise ValueError('Invalid adc value provided')
    
    def _eps_read_channel_single_ended(self,eps_ch):
        adc_ch = (eps_ch+1) % 8 - 1
        adc_num = None

        for adc in self.AdcChannelScope:
            if eps_ch in adc.value:
                adc_num = int(adc.name.replace('ADC_',''))
        print(f'EPS_CH: {eps_ch}, ADC_CH: {adc_ch}, ADC_NUM: {adc_num}')
        raise ValueError('Provided EPS ADC channel (in scope of EPS global scope assignments) did not match any of the assignments in AdcChannelScope(Enum)')

        

                # return _adc_read_channel_single_ended(adc.name,)


eps = EddyEps(smbus_num=1)

for i in range(17):
    eps._eps_read_channel_single_ended(i)
