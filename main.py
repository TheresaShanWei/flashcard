#!/usr/bin/python
import json
import os
import random

wordpath = "./wordlist.json"
reviewpath = "./reviewlist.json"


# 保存数据
def save(model, path):
    # model = {}  # 数据
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(model, json_file, ensure_ascii=False)


# 读取数据
def read(path):
    try:
        with open(path, 'r', encoding='utf-8') as json_file:
            model = json.load(json_file)
    except Exception as e:
        save({}, path)
        model = {}
    return model


# 进入主循环
while True:
    # 接受输入指令
    directive = input("请输入指令（按回车后执行）：")
    # 去掉空格转化小写
    directive = directive.strip().lower()
    if directive.startswith('input='):
        # input = key = value
        # 处理输入 keyvalue命令
        ipt = directive.split("=")
        if len(ipt) < 3:
            print("输入有误，请检查后再输入，输入‘help’获取命令列表")
            continue
        current = read(wordpath)
        current[ipt[1]] = ipt[2]
        save(current, wordpath)
        print("保存成功")
    elif directive.startswith('loadfile='):
        # loadfile = path
        # 处理输入 加载文件命令
        ipt = directive.split("=")
        if len(ipt) < 2:
            print("输入有误，请检查后再输入，输入‘help’获取命令列表")
            continue
        if not os.path.exists(ipt[1]):
            print("文件路径不存在，请检查后再输入")
            continue
        try:
            rd = read(ipt[1])
        except Exception as e:
            print(ipt[1], "文件格式错误，请检查后再试")
            continue
        wli = read(wordpath)
        newli = dict(wli, **rd)
        save(newli, wordpath)
    elif directive.startswith('modify='):
        # modify=key=value
        ipt = directive.split("=")
        if len(ipt) < 3:
            print("输入有误，请检查后再输入，输入‘help’获取命令列表")
            continue
        current = read(wordpath)
        if current.get(ipt[1]):
            current[ipt[1]] = ipt[2]
            save(current, wordpath)
            print("modify succes")
        else:
            print("Can not find this word, please add to the flash card first")
    elif directive.startswith('dlist='):
        # deletelist=wordlist
        ipt = directive.split("=")
        if len(ipt) < 2:
            print("输入有误，请检查后再输入，输入‘help’获取命令列表")
            continue
        if  'word' in ipt[1]:
            save({}, wordpath)
            print("删除wordlist成功")
        elif  'review' in ipt[1]:
            save({}, reviewpath)
            print("删除reviewlist成功")
        else:
            print("命令有误：只能删除wordlist/reviewlist")
    elif directive.startswith('delete='):
        # delete = key
        ipt = directive.split("=")
        if len(ipt) < 2:
            print("输入有误，请检查后再输入，输入‘help’获取命令列表")
            continue
        if current.get(ipt[1]):
            current.pop(ipt[1])
            save(current, wordpath)
            print("delete succes")
        else:
            print("We do not have this word in the wordlist")
    elif directive.startswith('search='):
        # search=key
        ipt = directive.split("=")
        if len(ipt) < 2:
            print("输入有误，请检查后再试，输入‘help’获取命令列表")
            continue
        current = read(wordpath)
        if current.get(ipt[1]):
            print(ipt[1], "：", current.get(ipt[1]))
        else:
            print("We do not have this word in the wordlist")
    elif directive.startswith('review'):
        current = read(reviewpath)
        if current:
            for key in current:
                print(key, '：', current[key])
        else:
            print("没有复习的单词")
    elif directive.startswith('words'):
        current = read(wordpath)
        if current:
            for key in current:
                print(key, '：', current[key])
        else:
            print("单词库为空")
    elif directive.startswith('quiz='):
        # 命令: quiz=numb,说明：随机选取numb条单词复习
        ipt = directive.split("=")
        if len(ipt) < 2:
            print("输入有误，请检查后再试，输入‘help’获取命令列表")
            continue
        if not ipt[1].isdigit():
            print("输入格式有误或者为非数字，请检查后再试")
            continue
        current = read(wordpath)

        ret = []
        for key in range(int(ipt[1])):
            # 还有一个随机删除
            if not current:
                print("测试完所有单词")
                continue
            key = random.sample(current.keys(), 1)[0]
            value = current[key]
            current.pop(key)
            iptk = input(str(value)+ "：")
            if iptk == key:
                reviewli = read(reviewpath)
                if key in reviewli:
                    reviewli.pop(key)
                    save(reviewli, reviewpath)
            else:
                reviewli = read(reviewpath)
                if key not in reviewli:
                    reviewli[key] = value
                    save(reviewli, reviewpath)
            # 结果保存起来
            ret.append(key + "/" + iptk + "：" + str(iptk == key))
        # 结束打印结果
        for item in ret:
            print(item)
    elif directive.startswith('quit'):
        print("退出程序")
        break
    elif directive.startswith('help'):
        help = """
    input(添加): input=key=value
    loadfile(加载文件): loadfile=filePath
    modify(修改): modify=key=value
    dlist(批量删除): dlist=words/reviewlist
    delete(删除)：delete=key
    search(查找)：search=key
    review(查看)：review
    words(查看)：words
    quiz(测试)：quiz=number
    quit(退出)：quit
    help(帮助)：help
    """
        print("help:",help)
        pass
    else:
        print("命令输入有误，请检查后再试，发送help获取帮助")
