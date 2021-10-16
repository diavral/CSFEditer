#-*- decoding: utf-8 -*-#
# coding or decoding?Just use unicode?
# filename:    test
# author:   1
# created:   2021/10/10の19:09
# finished:
# 标准库
from binascii import unhexlify
from json import dumps,loads
# 第三方库
# 模块
try:
    from code import cache
except:
    pass


filepath='ra2md.csf'


def func_decode(a0: bytes = b"\xb4\x92*tQ\xb2g\xba") -> str:
    """
    解码函数
    将每个DWORD的字节用0XFF去减，然后换大小端，就得到Unicode_escape可以解码的字节串，然后以utf-8格式返回
    """
    temp1,is_odd,result = None, True, ''
    for i in a0:
        if is_odd:
            temp1=0xff-i
            is_odd=False
        else:
            is_odd=True
            result += chr((0xff-i)*16*16+temp1)
    return result


def func_number_decode(a0: bytes = b'\x00\x00\x00\x00') -> int:
    """
    将DWORD大小端互换，然后转为10进制
    """
    temp1,is_odd,result = None, True, []
    for i in a0:
        if is_odd:
            temp1=i
            is_odd=False
        else:
            is_odd=True
            result.append((i)*16*16+temp1)
    return result[0]


def func_encode(a0: str = '测试䶮䖘') -> bytes:
    """
    编码函数
    将utf-8的每个字转换为十进制数，再转十六进制，换大小端，用0XFF去减每个字节
    """
    result=[]
    for i in a0:
        temp = hex(ord(i)).split('0x')[-1].zfill(4)
        result.append((0xff-eval('0x'+temp[2:])))
        result.append((0xff - eval('0x' + temp[0:2])))
    return bytearray(result)


def func_read_label_value(body:bytes) -> (bytes,dict):
    if len(body)>0:
        label_1=body[0:4]  # b' LBL' 标签头
        label_2=body[4:8]  # 字符串对数，一般是1
        label_3=body[8:12]  # 后面数据的大小
        label_length = 12+func_number_decode(label_3)
        label_4 = body[12:label_length]  # 可变长度，是字符串，且是gbk,用utf-8或unicode_escape解不了

        value_1=body[label_length:label_length+4]  # RTS   WRTS

        if value_1 == b'WRTS':
            value_2 = body[label_length + 4 :label_length + 8]  # 后面数据的大小
            value_length = func_number_decode(value_2) * 2 + label_length + 8
            value_3 = body[label_length + 8 :value_length]  # 可变长度,必须解码，全是是Unicode
            value_4 = body[value_length :value_length + 4]  # 4位，储存后面的长度，由WRTS决定是否存在
            ex_length = func_number_decode(value_4)+value_length+4
            value_5 = body[value_length + 4 :ex_length]  # 可变长度，是字符串

            return (body[ex_length:],{"Label": label_4.decode("gbk") ,
                                      "Value" : func_decode(value_3) ,  "ExValue" : value_5.decode("gbk")})
        else:
            value_2=body[label_length+4:label_length+8]
            value_length=func_number_decode(value_2)*2+label_length+8
            value_3=body[label_length+8:value_length]
            return (body[value_length :] , { "Label" : label_4.decode("gbk") ,
                                          "Value" : func_decode(value_3), "ExValue" : ""})


def simplify(all_content) :
    to_new_content = set()
    new_content = {}
    for index in all_content :
        if '_' in index['Label'] and ':' not in index['Label'] :
            print(index)
            to_new_content.add(index['Label'].split('_')[0])
        else :
            to_new_content.add(index['Label'].split(':')[0])
    print(to_new_content)
    for index2 in to_new_content :
        new_content[index2] = []
    for index3 in all_content :
        if '_' in index3['Label'] and ':' not in index3['Label'] :
            tempSet = []
            tempSet.append(index3['Label'].split('_' , 1)[-1])
            tempSet.append(index3['Value'])
            tempSet.append(index3['ExValue'])
            new_content[index3['Label'].split('_')[0]].append(tempSet)
        else :
            tempSet = []
            tempSet.append(index3['Label'].split(':')[-1])
            tempSet.append(index3['Value'])
            tempSet.append(index3['ExValue'])
            new_content[index3['Label'].split(':')[0]].append(tempSet)

    return to_new_content , new_content


def read_file(filename) :
    with open(file=filename , mode='rb') as f :
        file_content = f.read()

    # 文件头
    header=file_content[0:24]
    header_1=header[0:4]  # b' FSC' 文件头
    header_2=header[4:8]  # 版本 = 3,在红警里面
    header_3=header[8:12]  # 标签数
    header_4=header[12:16]  # value数，等于header_3,单纯的键值对
    header_5=header[16:20]  # 未使用,可以用作字处理软件的标记
    header_6=header[20:24]  # 语言 已发布* ::= 0->美* 1->英 2->德* 3->法* 4->西 5->意 6->日 7->无 8->韩* 9->汉* 大于9->未知

    # 用于展示
    csf_version=func_number_decode(header_2)
    all_counts=func_number_decode(header_3)
    csf_language=func_number_decode(header_6)
    csf_software=func_decode(header_5)

    # 标签
    body=file_content[24:]
    all_content=[]
    while len(body)>0:
        temp=func_read_label_value(body)
        all_content.append(temp[-1])
        body=temp[0]

    # todo:在新的函数读取json，并转码保存
    with open('cacheTemp.py','a+',encoding='utf-8') as f:
        f.write('test_cache='+str(all_content)+'\n')


def write_file(filename=None, json_dict=None):

    with open(file=filename , mode='ab+') as f :

        # file header
        all_counts=unhexlify(hex(len(json_dict)).split('0x')[-1].zfill(4))[::-1]+b'\x00\x00'
        csf_version=b'\x03\x00\x00\x00'
        csf_software=b'\x09\x00\x00\x00'
        csf_language=b'\x09\x00\x00\x00'
        file_header=b' FSC'+csf_version+all_counts+all_counts+csf_software+csf_language

        f.write(file_header)

        label_fix = b' LBL'
        label_couples = b'\x01\x00\x00\x00'
        for index in json_dict:
            label_length = unhexlify(hex(len(index['Label'].encode('gbk'))).split('0x')[-1].zfill(4))[::-1]+b'\x00\x00'
            label_content = index['Label'].encode('gbk')
            label_format = label_fix + label_couples + label_length + label_content
            if len(index['ExValue'])>0:
                value_type = b'WRTS'
                value_length = unhexlify(hex(len(index['Value'])).split('0x')[-1].zfill(4))[::-1]+b'\x00\x00'
                value_content = func_encode(index['Value'])
                value_ex_length = unhexlify(hex(len(index['ExValue'])).split('0x')[-1].zfill(4))[::-1]+b'\x00\x00'
                value_ex_content = index['ExValue']
                value_format = value_type + value_length + value_content + value_ex_length + value_ex_content
            else:
                value_type=b' RTS'
                value_length=unhexlify(hex(len(index['Value'])).split('0x')[-1].zfill(4))[::-1]+b'\x00\x00'
                value_content=func_encode(index['Value'])
                value_format = value_type + value_length + value_content

            f.write(label_format+value_format)




read_file(filepath)
# write_file('ra2dm.csf',cache.test_cache)