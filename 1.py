data = '''multi_nics_hotplug).nic_virtio
multi_nics_hotplug).sameid
virtio_fs_readonly
virtio_fs_share_data).default.default.with_cache.always.default.default
dump_guest_memory).verify_diff_format_dump_file.query_dump_guest_memory_capability
dump_guest_memory).verify_diff_format_dump_file.quux_format_dump
dump_guest_memory).verify_diff_format_dump_file.paging_true_snappy_format_dump
dump_guest_memory).verify_diff_format_dump_file.paging_true_zlib_format_dump
dump_guest_memory).verify_diff_format_dump_file.paging_true_lzo_format_dump
'''

data1 = data.replace('\n', ',').replace('\r', ',').replace(')', '')
# data1 = data.replace('\n', ' ').replace('\r', ' ')
# print(data1)
print(data1)
data1 = data1.split(',')
# print(data1)
# for i in data1:
#     print('mdevctl undefine --uuid '+i)