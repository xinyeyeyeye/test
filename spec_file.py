from specfile import Specfile
import re
spec_file_src='/usr/yxy/7zip.spec'



class specfile_analyse(object):
    def __init__(self):
        self.define_dict={}
        self.bcond_with_list=[]
        self.bcond_without_list=[]
        self.spec_file=''

    def get_specfile(self,filepath):
        self.spec_file = Specfile(filepath)

    def replace_define(self,String):
        query = re.findall(r"\%{(.*?)\}", String)
        for q in query:
            replace_str=self.define_dict.get(q,'')
            if not replace_str:
                continue
            str(String).replace('${'+q+'}',replace_str)
        return String
    def get_define_and_bcond(self):
        if not self.spec_file:
            return
        with self.spec_file.tags() as tags:
            for tag in tags:
                for t in tag.comments.get_raw_data():
                    if '#define' in t:
                        t=t.split(' ')
                        self.define_dict.update({self.replace_define(t[1]):self.replace_define(t[2])})
                    if '%bcond_with' in t:
                        t=t.split(' ')
                        self.bcond_with_list.append(t[1])
                    if '%bcond_without' in t:
                        t = t.split(' ')
                        self.bcond_without_list.append(t[1])
                    if '%global' in t:
                        t = t.split(' ')
                        self.define_dict.update({self.replace_define(t[1]):self.replace_define(t[2])})
            self.define_dict.update({
                'name':tags.name.value,
                'version':tags.version.value,
            })

    def analyse_if(self,tags,index):
        value_list=[]
        result_dict={}
        child_list=[]
        if_first_visit=True
        handed_index=-1
        handing_tag_name = tags[index].name.lower()
        for i in range(index,len(tags)):
            if handed_index!=-1:
                if i<handed_index:
                    continue
            for t in tags[i].comments.get_raw_data():
                if '%ifarch' or '%ifnoarch' in t:
                    if if_first_visit:
                        t=self.replace_define(t).splite(' ')
                        result_dict['condition']=t[0]
                        result_dict['arch']=t[1:len(t)-1]
                        if_first_visit=False
                    else:
                        child=self.analyse_if(tags,i)
                        child_list.append(child)
                    break
                elif '%if' in t:
                    if if_first_visit:
                        t = self.replace_define(t).replace('%if','')
                        result_dict['condition']=t
                        if_first_visit=False
                    else:
                        child,handed_index=self.analyse_if(tags,i)
                        child_list.append(child)
                    break
                elif '%endif' in t:
                    if len(value_list) != 1:
                        result_dict.update({handing_tag_name: value_list})
                    else:
                        result_dict.update({handing_tag_name: value_list[0]})
                    result_dict.update({'child':child_list})
                    return result_dict,i
            if handing_tag_name != tags[i].name.lower():
                if len(value_list) != 1:
                    result_dict.update({handing_tag_name: value_list})
                else:
                    result_dict.update({handing_tag_name: value_list[0]})
                handing_tag_name = tags[i].name.lower()
                value_list = []
            else:
                value_list.append(tags[i].value)

    def get_data(self,filepath):
        self.get_specfile(filepath)
        self.get_define_and_bcond()
        data_dict={}
        handed_index = -1
        with self.spec_file.tags() as tags:
            handing_tag_name=tags[0].name.lower()
            value_list=[]
            for i in range(0,len(tags)):
                if handed_index != -1:
                    if i < handed_index:
                        continue
                if handing_tag_name!=tags[i].name.lower():
                    if len(value_list)!=1:
                        data_dict.update({handing_tag_name:value_list})
                    else:
                        data_dict.update({handing_tag_name:value_list[0]})
                    handing_tag_name=tags[i].name.lower()
                    value_list=[]
                for t in tags[i].comments.get_raw_data():
                    if '%if' in t:
                        if_analyse_dict,handed_index=self.analyse_if(tags,i)
                        print(if_analyse_dict)
                        break
test=specfile_analyse()
test.get_data(spec_file_src)