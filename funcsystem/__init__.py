load_object = None

while load_object is None:
    pass

if load_object == 'function_mapping':
    from funcsystem.map import function_mapping
    print('函数测绘加载完毕...')
else:
    from funcsystem.factory import function_factory_main
    print('函数工厂加载完毕...')
