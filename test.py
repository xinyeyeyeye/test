import os
import json
file_path='C:\\Users\\yangx\\Desktop\\openHarmony组件\\openHarmony所有组件'#'C:\\Users\\yangx\\Desktop\\openHarmony组件\\支持RISCV组件'
result_list=[]
for path, dir_names, file_names in os.walk(file_path):
    for file_name in file_names:
        if file_name.endswith('.json'):
            print(path+'\\'+file_name)
            with open(path+'\\'+file_name, 'r', encoding='utf-8') as f:
                context = f.read()
                js = json.loads(context)
                subsystem_list = js['subsystems']
                for subsystem in subsystem_list:
                    component_list=subsystem['components']
                    for component in component_list:
                        result_list.append(component['component'])
print(len(result_list))
result_list=list(set(result_list))
print(result_list)
print(len(result_list))
