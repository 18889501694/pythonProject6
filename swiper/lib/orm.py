"""
当访问一个对象的会根据不同的情况作不同的处理，是比较复杂的。
一般象a.b这样的形式，python可能会先查找a.__dict__中是否存在，如果不存在会在类的__dict__中去查找，再没找到可能会去按这种方法去父类中进行查找。
实在是找不到，会调用__getattr__，如果不存在则返回一个异常。那么__getattr__只有当找不到某个属性的时候才会被调用。
因此，你可能会想实现一种机制，当访问一个不存的属性时，自动提供一个缺省值。
"""

from datetime import time, datetime


class ModelMixin:
    def to_dict(self, ignore=()):
        """将model对象转化成dict"""

        data = {}
        for field in self._meta.fields:
            name = field.attname  # 获取字段名
            value = self.__dict__[name]  # 获取对象属性
            if name in ignore:
                continue
            # print(name.value)
            # 检查传入的数据能否被序列化
            if isinstance(value, (datetime, data, time)):
                # value=getattr(self,name)
                data[name] = value  # 生成字典
        return data
