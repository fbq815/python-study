# 类是某一批对象的抽象，可以把类理解成某种改年
# 对象才是一个具体存在的东西
'''
class 类名:
    执行语句
    零到多个类变量
    零到多个方法
'''


class User:
    '''最简单的user类
    '''
    print('user类')

# Item类


class Item:
    '''Item类
    '''
    print('Item类')
    # 类空间中定义的变量，属于类变量
    itemtype = '电子产品'
    itemcolor = '未知'


print(Item.itemcolor)
print(Item.itemtype)


class Book:
    print('book')
    booktype = 'IT图书'

    # 定义方法与定义函数几乎一样
    # 实例方法，第一个参数推荐使用self（并不强制）， 这样有更好的可读性
    def desc(self):
        self.name = '疯狂python将一'
        self.price = 118
        print('图书是%s,价格是%d') % (self.name,self.price)

    def haha(self):
        print('我只是一个哈哈方法')
 # raise virt_vm.VMSMPTopologyInvalidError(smp_err)
a = 4
b = 4
c = 3
a = a or b - c
print(a)
