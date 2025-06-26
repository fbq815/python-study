libvirtd_debug_level = "1"
libvirtd_log_cleanup = "no"
variants:
    - @cpu:
        only virsh.setvcpus.normal_test.guest_on.name_option.restart_vm.update_cur
    - @block:
        only virtual_disks.multidisks.coldplug.multi_disks_test.disk_virtio_scsi_multi_queue
    - @storage_vm_migration:
        only backingchain.blockcommit.basic_function.commit_tb.block_disk
    - @guest_agent:
        only virsh.domtime.positive.set_time_now
        local_ip = localhost
        local_pwd = kvmautotest
        remote_ip =localhost
        remote_pwd = kvmautotest
    - @cleanup:
        only remove_guest.without_disk