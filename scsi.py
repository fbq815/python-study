data = '''rng_maxbytes_period).positive_test.maxbytes_512_period_1k
rng_maxbytes_period).positive_test.maxbytes_1024_period_1k
rng_maxbytes_period).positive_test.maxbytes_1024k_period_1m
'''

data1 = data.replace('\n', ',').replace('\r', ',').replace(')', '').replace('.s390-virtio','')
# data1 = data.replace('\n', ' ').replace('\r', ' ')
# data1 = data.replace(' ', '\n').replace(' ', '\r')
# print(data1)
print(data1)
data1 = data1.split(',')
# print(data1)
# for i in data1:
#     print('mdevctl undefine --uuid '+i)