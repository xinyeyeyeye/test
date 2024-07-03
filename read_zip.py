import zipfile
import json

filepath='C:/Users/yangx/Desktop/Specs-master.zip'
if zipfile.is_zipfile(filepath):
    #with zipfile.ZipFile(filepath,'r') as f:
    #    print(f.infolist())
    zip_file=zipfile.ZipFile(filepath,'r')
    json_list = []
    for name in zip_file.namelist():
        if name.endswith('.json'):
            json_list.append(name)
    i=0
    project_name=json_list[0].split('/')[-3]
    project_version_list=[]
    for j in json_list:
        n=j.split('/')[-3]
        if project_name==n:
            content=zip_file.open(j)
            content=json.load(content)
            project_version_list.append(content)
        if project_name!=n:
            project_name=n
            print(project_version_list)
            project_version_list=[]
            content = zip_file.open(j)
            content = json.load(content)
            project_version_list.append(content)
        if i >100:
            break
        i=i+1
