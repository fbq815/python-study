data = '''qemu_guest_agent).virtio_serial.check_get_interfaces
nicdriver_unload
'''

data1 = data.replace('\n', ',').replace('\r', ',').replace(')', '')
# data1 = data.replace('\n', ' ').replace('\r', ' ')
# print(data1)
print(data1)
data1 = data1.split(',')
# print(data1)
# for i in data1:
#     print('mdevctl undefine --uuid '+i)

