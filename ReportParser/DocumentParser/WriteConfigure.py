import ConfigParser
import os

config = ConfigParser.ConfigParser()


config.add_section('Functionality')
config.set('Functionality','FT1','myRIO_Functionality No SPI and I2C Test-Suite Report')
config.set('Functionality','FT2','myRIO_Functionality Only SPI and I2C Test-Suite Report')
config.set('Functionality','FT3','myRIO_Module Integration Testing Test-Suite Report')

config.add_section('Performance')
config.set('Performance','PT1','myRIO fixedPersonality Performance No SPI_I2C Test-Suite Report')
config.set('Performance','PT2','myRIO ID instrumentDrivers Performance Test-Suite Report')
config.set('Performance','PT3','myRIO expressVI Performance Test-Suite Report')
config.set('Performance','PT4','myRIO ID I2CSPI Performance Test-Suite Report')

config.add_section('AI\Test_FP AI read all channels.vi')
config.set('AI\Test_FP AI read all channels.vi','Avg Read (ms)','0.02615')

config.add_section('AI\Test_FP AI read and open all channels.vi')
config.set('AI\Test_FP AI read and open all channels.vi','Avg Read (ms)','271.6')

config.add_section('AI\Test_FP AI read single channel.vi')
config.set('AI\Test_FP AI read single channel.vi','Avg Read (ms)','0.00097')

config.add_section('AO\Test_FP AO write all channels.vi')
config.set('AO\Test_FP AO write all channels.vi','Avg Read (ms)','0.00287')

config.add_section('AO\Test_FP AO write and open all channels.vi')
config.set('AO\Test_FP AO write and open all channels.vi','Avg Read (ms)','269.8')

config.add_section('AO\Test_FP AO write single channel.vi')
config.set('AO\Test_FP AO write single channel.vi','Avg Read (ms)','0.00077')

config.add_section('Control Loop\AI+AO\Test_FP Control Loop AI+AO.vi')
config.set('Control Loop\AI+AO\Test_FP Control Loop AI+AO.vi','Avg Read (ms)','0.04282')

config.add_section('DIO\Test_FP DIO read all channels.vi')
config.set('DIO\Test_FP DIO read all channels.vi','Avg Read (ms)','0.00328')

config.add_section('DIO\Test_FP DIO read_write all channels.vi')
config.set('DIO\Test_FP DIO read_write all channels.vi','Avg Read (ms)','0.00468')

config.add_section('DIO\Test_FP DIO write all channels.vi')
config.set('DIO\Test_FP DIO write all channels.vi','Avg Read (ms)','0.00465')

config.add_section('AI\Test_ID AI read all channels.vi')
config.set('AI\Test_ID AI read all channels.vi','Avg Read (ms)','0.01898')

config.add_section('AI\Test_ID AI read and open all channels.vi')
config.set('AI\Test_ID AI read and open all channels.vi','Avg Read (ms)','316.3')

config.add_section('AI\Test_ID AI read and open single channel.vi')
config.set('DIO\Test_FP DIO read_write all channels.vi','Avg Read (ms)','315.8')

config.add_section('AI\Test_ID AI read single channel.vi')
config.set('AI\Test_ID AI read single channel.vi','Avg Read (ms)','0.00771')

config.add_section('AO\Test_ID AO read all channels.vi')
config.set('AO\Test_ID AO read all channels.vi','Avg Read (ms)','0.02146')

config.add_section('AO\Test_ID AO read and open all channels.vi')
config.set('AO\Test_ID AO read and open all channels.vi','Avg Read (ms)','318.9')

config.add_section('AO\Test_ID AO read and open single channel.vi')
config.set('AO\Test_ID AO read and open single channel.vi','Avg Read (ms)','316')

config.add_section('AO\Test_ID AO read single channel.vi')
config.set('AO\Test_ID AO read single channel.vi','Avg Read (ms)','0.01654')

config.add_section('DI\Test_ID DI read all channels.vi')
config.set('DI\Test_ID DI read all channels.vi','Avg Read (ms)','0.14')

config.add_section('DI\Test_ID DI read and open all channels.vi')
config.set('DI\Test_ID DI read and open all channels.vi','Avg Read (ms)','328.1')

config.add_section('DI\Test_ID DI read and open single channel.vi')
config.set('DI\Test_ID DI read and open single channel.vi','Avg Read (ms)','315.9')

config.add_section('DI\Test_ID DI read single channel.vi')
config.set('DI\Test_ID DI read single channel.vi','Avg Read (ms)','0.09')

config.add_section('DO\Test_ID DO write all channels.vi')
config.set('DO\Test_ID DO write all channels.vi','Avg Read (ms)','0.1')

config.add_section('DO\Test_ID DO write single channel.vi')
config.set('DO\Test_ID DO write single channel.vi','Avg Read (ms)','0.1')

config.add_section('PWM\Test_ID PWM All Parallel Loop Rate.vi')
config.set('PWM\Test_ID PWM All Parallel Loop Rate.vi','Avg Read (ms)','0.01257')

config.add_section('PWM\Test_ID PWM All Single Loop Rate.vi')
config.set('PWM\Test_ID PWM All Single Loop Rate.vi','Avg Read (ms)','0.1214')

config.add_section('PWM\Test_ID PWM Loop Rate.vi')
config.set('PWM\Test_ID PWM Loop Rate.vi','Avg Read (ms)','0.01254')

config.add_section('PWM\Test_ID PWM Open and Read Loop Rate.vi')
config.set('PWM\Test_ID PWM Open and Read Loop Rate.vi','Avg Read (ms)','315.8')

config.add_section('QE\Test_ID QE read and open single channel.vi')
config.set('QE\Test_ID QE read and open single channel.vi','Avg Read (ms)','317.3')

config.add_section('QE\Test_ID QE read single channel.vi')
config.set('QE\Test_ID QE read single channel.vi','Avg Read (ms)','3.35')

config.add_section('QE\Test_ID QE read two channels.vi')
config.set('QE\Test_ID QE read two channels.vi','Avg Read (ms)','3.52')

config.add_section('AI\Test_EVI AI read all channels with preopen.vi')
config.set('AI\Test_EVI AI read all channels with preopen.vi','Avg Read (ms)','0.02011')

config.add_section('AI\Test_EVI AI read all channels.vi')
config.set('AI\Test_EVI AI read all channels.vi','Avg Read (ms)','0.02345')

config.add_section('AI\Test_EVI AI read single channel with preopen.vi')
config.set('AI\Test_EVI AI read single channel with preopen.vi','Avg Read (ms)','0.0091')

config.add_section('AI\Test_EVI AI read single channel.vi')
config.set('AI\Test_EVI AI read single channel.vi','Avg Read (ms)','0.01228')

config.add_section('AO\Test_EVI AO write all channels with preopen.vi')
config.set('AO\Test_EVI AO write all channels with preopen.vi','Avg Read (ms)','0.03042')

config.add_section('AO\Test_EVI AO write all channels.vi')
config.set('AO\Test_EVI AO write all channels.vi','Avg Read (ms)','0.03391')

config.add_section('AO\Test_EVI AO write single channel with preopen.vi')
config.set('AO\Test_EVI AO write single channel with preopen.vi','Avg Read (ms)','0.02454')

config.add_section('AO\Test_EVI AO write single channel.vi')
config.set('AO\Test_EVI AO write single channel.vi','Avg Read (ms)','0.02771')

config.add_section('DIO\Test_EVI DI ReadAllInLoop.vi')
config.set('DIO\Test_EVI DI ReadAllInLoop.vi','Avg (ms)','0.1472')

config.add_section('DIO\Test_EVI DI ReadOneInLoop.vi')
config.set('DIO\Test_EVI DI ReadOneInLoop.vi','Avg (ms)','0.09413')

config.add_section('DIO\Test_EVI DO WriteAllInLoop.vi')
config.set('DIO\Test_EVI DO WriteAllInLoop.vi','Avg (ms)','0.1024')

config.add_section('DIO\Test_EVI DO WriteOneInLoop.vi')
config.set('DIO\Test_EVI DO WriteOneInLoop.vi','Avg (ms)','0.0786')

config.add_section('Test_ID SPI read write multiple sample loopback.vi')
config.set('Test_ID SPI read write multiple sample loopback.vi','Avg Read (ms)','26.19')

config.add_section('Test_ID SPI read write single sample loopback.vi')
config.set('Test_ID SPI read write single sample loopback.vi','Avg Read (ms)','16.53')

config.add_section('Test_ID SPI write and open multiple samples.vi')
config.set('Test_ID SPI write and open multiple samples.vi','Avg Read (ms)','4294941')

config.add_section(' Test_ID SPI write and open single sample.vi')
config.set(' Test_ID SPI write and open single sample.vi','Avg Read (ms)','16.86')

config.add_section('Test_ID SPI write multple samples.vi')
config.set('Test_ID SPI write multple samples.vi','Avg Read (ms)','26.19')

config.add_section('Test_ID SPI write single sample.vi')
config.set('Test_ID SPI write single sample.vi','Avg Read (ms)','16.85')


config.write(open('../../Configure.ini','w'))