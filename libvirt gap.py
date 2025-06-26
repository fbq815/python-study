libvirtd_debug_level = "1"
libvirtd_log_cleanup = "no"
variants:
    - @prepare:
        only unattended_install.cdrom.extra_cdrom_ks.default_install.aio_threads
    - @mem:
        only setmem.memballoon_option.with_packed_on
    - @block:
        only virtual_disks.multidisks.coldplug.multi_disks_test.disk_virtio_scsi_multi_queue
    - @storage_vm_migration:
        only backingchain.blockcommit.basic_function.commit_tb.block_disk
    - @chardev:
        only controller.functional.positive_tests.virtio_serial_0_vectors controller.functional.positive_tests.virtio_serial
    - @guest_agent:
        only virsh.domtime.positive.set_time_now
        local_ip = localhost
        local_pwd = kvmautotest
        remote_ip =localhost
        remote_pwd = kvmautotest
    - @cleanup:
        only remove_guest.without_disk