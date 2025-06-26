data = '''nfs_corrupt.with_qcow2_format
nfs_corrupt.with_raw_format
nfs_corrupt.with_luks_format
stop_continue.with_file_copy
dd_test.readwrite.zero2disk
dd_test.readwrite.disk2null
virtual_nic.private
netperf_stress_test.TCP_STREAM.guest2guest
netperf_stress_test.TCP_STREAM.host2guest
nicdriver_unload
vlan.vlan_connective_test
vlan.vlan_scalability_test
ping.default_ping
ping.ext_host
balloon_service.small_polling_interval
ksm_base.base
qemu_disk_img_compare
qemu_disk_img.convert.base_to_qcow2.default.default
'''
# data1 = data.replace('\n', ',').replace('\r', ',')
data1 = data.replace('\n', ',').replace('\r', ',')
# print(data1)
print(data1)
data1 = data1.split(',')
# print(data1)
# for i in data1:
#     print('mdevctl undefine --uuid '+i)