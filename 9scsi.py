data = '''kdump).one_vm.with_stress.netperf_stress.default
flow_caches_stress_test).multi_queues
'''

data1 = data.replace('\n', ',').replace('\r', ',').replace(')', '')
# data1 = data.replace('\n', ' ').replace('\r', ' ')
# print(data1)
print(data1)
data1 = data1.split(',')
# print(data1)
# for i in data1:
#     print('mdevctl undefine --uuid '+i)

