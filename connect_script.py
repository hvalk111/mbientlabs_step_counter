from mbientlab.metawear import MetaWear, libmetawear
from mbientlab.metawear.cbindings import *

device = MetaWear('00:1A:7D:DA:71:13')
device.connect()
