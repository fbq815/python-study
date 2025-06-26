import re
qtree_info = '''
dev: virtio-net-ccw, id "idopJG2L"
ioeventfd = true
max_revision = 2 (0x2)
devno = "<unset>"
dev_id = "fe.0.0001"
subch_id = "fe.0.0001"
bus: virtio-bus
type virtio-ccw-bus
dev: virtio-net-device, id ""
csum = true
guest_csum = true
gso = true
guest_tso4 = true
guest_tso6 = true
guest_ecn = true
guest_ufo = true
guest_announce = true
host_tso4 = true
host_tso6 = true
host_ecn = true
host_ufo = true
mrg_rxbuf = true
status = true
ctrl_vq = true
ctrl_rx = true
dev: virtio-scsi-ccw, id "virtio_scsi_ccw0"
  ioeventfd = true
  max_revision = 2 (0x2)
  devno = "<unset>"
  dev_id = "fe.0.0000"
subch_id = "fe.0.0000"
bus: virtio-bus
type virtio-ccw-bus
'''
ccw_info = '0.0.0000  0.0.0001  0.0.0002  0.0.0003  0.0.0004'
ccw_info = '''
Device   Subchan.  DevType CU Type Use  PIM PAM POM  CHPIDs           
0.0.0000 0.0.0000  0000/00 3832/08 yes  80  80  ff   00000000 00000000
0.0.0001 0.0.0001  0000/00 3832/01 yes  80  80  ff   00000000 00000000
0.0.0002 0.0.0002  0000/00 3832/12 yes  80  80  ff   00000000 00000000
0.0.0003 0.0.0003  0000/00 3832/12 yes  80  80  ff   00000000 00000000
ccw_n = re.findall(ccw_id_pattern, ccw_info)[0]
'''

a_pattern = r"dev_id = (.*?)"
a = re.findall(r'dev:virtio-scsi-ccw.*\n.*\n.*\n.*\ndev_id='
               '\"fe.0.(.*?)\"',
               qtree_info.replace(' ', ''))[0]
print(a)
# x = re.findall('"query": "(.*?)","slotList"', r.text)
ccw_id_pattern = "\d+\.\d+\."
ccw_id_pattern = \
    ccw_id_pattern + '%s' % \
    re.findall('dev:virtio-scsi-ccw.*\n.*\n.*\n.*\ndev_id='
               '\"fe.0.(.*?)\"',
               qtree_info.replace(' ', ''))[0]
print(ccw_id_pattern)
ccw_n = re.findall(ccw_id_pattern, ccw_info)[0]
if not ccw_n:
    print(False)

#                     ccw_id_pattern = "\d+\.\d+\."
#                     ccw_id_pattern = ccw_id_pattern +'%d' %
#ccw_n = 0.0.0000
# b = r"dev_id = \"fe.0.*?\""
# dev_id = "fe.0.0001"\n
'''
/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
/etc/pki/ca-trust/source/anchors/RH-IT-Root-CA.crt
/etc/pki/ca-trust/source/ca-bundle.legacy.crt
/etc/pki/tls/certs/ca-bundle.crt
/etc/pki/tls/certs/ca-bundle.trust.crt
/usr/share/doc/python3-pycurl/tests/certs/ca.crt
/usr/share/doc/python3-pycurl/tests/certs/server.crt
/usr/share/pki/ca-trust-legacy/ca-bundle.legacy.default.crt
/usr/share/pki/ca-trust-legacy/ca-bundle.legacy.disable.crt
'''