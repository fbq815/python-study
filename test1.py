data = '''virtio_fs_share_data).run_stress.with_fio.with_cache.auto.default.default
virtio_fs_share_data).run_stress.with_fio.with_cache.auto.with_writeback.default
virtio_fs_share_data).run_stress.with_fio.with_cache.always.default.default
virtio_fs_share_data).run_stress.with_fio.with_cache.always.with_writeback.default
virtio_fs_share_data).run_stress.with_fio.with_cache.none.default.default
virtio_fs_share_data).run_stress.with_fio.inode_file_handles.prefer.default.default
virtio_fs_share_data).run_stress.with_fio.inode_file_handles.prefer.sandbox.chroot.default
virtio_fs_share_data).run_stress.with_fio.inode_file_handles.mandatory.default.default
virtio_fs_share_data).run_stress.with_fio.inode_file_handles.mandatory.sandbox.chroot.default
'''

data1 = data.replace('\n', ',').replace('\r', ',').replace(')', '')
# data1 = data.replace('\n', ' ').replace('\r', ' ')
# data1 = data.replace(' ', '\n').replace(' ', '\r')
# print(data1)
print(data1)
data1 = data1.split(',')
# print(data1)
# for i in data1:
#     print('mdevctl undefine --uuid '+i)