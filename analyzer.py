#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2017-05-09 by root@mail.zmblog.org

#简单C语言词法分析器，有基本分析、查错能力
#及大部分八、十六、十进制整数，指数型、非指数型浮点数判断

#缺陷：部分代码冗余，未精细判断字符、字符串型
#未对部分操作符二义性处理

import os
import sys
from functools import reduce

keyword=("auto","break","case","char","const" ,"continue" ,"default" ,"do",
         "double,","else","enum" ,"extern","float","for","goto","if",
         "int" ,"long", "register" ,"return", "short", "signed","sizeof","static",
         "struct","switch","typedef","union","unsigned","void","volatile","while")#关键字
delimiter=('(',')','[',']','{','}',';',',',' ','\'','"')#分隔符
operetor=('+','-','*','/','%','>','<','=','&','^','|','~','?',':','.','!')#操作符



def reader(filename):#读取
    try:
        file=open(filename,'r',encoding='utf-8')
        prog = file.read()#整篇读取，未分段处理
        if(prog==''):
            print("空文件")
        else:
            analyse(prog)
    except IOError as ioe:
        print("读取文件出错，请检测文件名及权限")
    except UnicodeDecodeError as e:
        print("文件格式错误")
    finally:file.close()
    pass

def skip(prog,flag):#跳过无效字符
    start=flag
    while prog[start]!='\n' and not prog[start].isspace() and not prog[flag]\
            in delimiter and not prog[start] in operetor:
        start += 1
    return start


def isdeli(ch) ->bool:#是否为（可跳过字符）或（不是分界符）
    return ch!='\n' and not ch.isspace() \
           and not ch in delimiter and not ch in operetor

def next(prog ,flag,ignore=False):
    #判断传入串flag位置后一个属性,以判断操作符是否二义性
    #ignore是否忽略空格
    start=flag+1
    if ignore:
        while prog[start]==" " or prog[start].isspace():
            start+=1
    if prog[start] in operetor:
        return "OPERETOR"
    elif prog[start] in delimiter:
        return "DELIMITER"
    elif prog[start].isalpha() or prog[start] == r'_':  # 标识符和关键字
        tmp = start
        while prog[start].isalnum() or prog[start] == r'_': start += 1
        fragment = str(reduce(lambda x, y: x + y, prog[tmp:start]))
        if fragment in keyword:  # 判断为关键字
            return "KEYWORD"
        else:  # 判断为标识符
            return "IDENTIFY"
    elif prog[start].isdigit():
        return "DIGIT"
        pass

def analyse(prog,befspace=0,flag=0,line=1):
    #分析函数，传入分析串，上一行位置，当前位置、行数
    length=len(prog)#字符长度
    print("LINE "+str(line)+" :",end=' ')
    while flag<length:#从左向右处理
        if prog[flag]=="#":#不考虑头文件及预编译
            flag+=1
            while prog[flag]!='\n' :#and prog[flag]!='\\'
                flag+=1
            print("< #,ignore >", end=' ')
        elif prog[flag]=='\n':#换行符结束
            line += 1  # 行数自增
            if flag-befspace>1:
                print()
                if (flag < length):
                    print("LINE " + str(line) + " :", end=' ')
            befspace=flag#上一行位置变，用于查错显示
            flag+=1#
        elif prog[flag].isspace():#空字符跳过
            flag+=1
        elif prog[flag].isalpha() or prog[flag]==r'_':#标识符和关键字
            tmp=flag
            while prog[flag].isalnum() or prog[flag]==r'_':flag+=1
            fragment=str(reduce(lambda x,y:x+y,prog[tmp:flag]))
            if fragment in keyword:#判断为关键字
                print("< "+fragment+",- >",end=' ')
            else:#判断为标识符
                print("< IDENTIFY,"+fragment+" >",end=' ')
        elif prog[flag].isdigit():#判断数字常量
            if prog[flag] == '0':#当开始字符为0
                if prog[flag+1].lower()=='x':#0x开头为十六进制
                    flag+=2
                    tmp=flag
                    while prog[flag].isdigit() or \
                            (prog[flag].lower()>='a' and prog[flag].lower()<='f'): #判断十六进制
                        flag+=1
                    numch=str(reduce(lambda x,y:x+y,prog[tmp:flag]))#拼接十六进制数字
                    num = str(int(numch, 16))#拼接为十进制数字
                    if prog[flag].lower()=='u' :#判断是否有符号、长整，当前flag指向十六进制后一位
                        if prog[flag+1].lower()=='l':#0x23ul
                            if prog[flag + 2].isalnum():#0x23uls报错，并跳过
                                print("<ERROR,INT_UN_LONG_DEFINE,LINE "+str(line)+" "+str(flag-befspace)+" >", end=' ')
                                flag += 3
                                flag = skip(prog, flag)
                            else:
                                print("< INT_UN_LONG,"+num+" >",end=' ')
                                flag+=2
                        elif prog[flag+1].isalnum():#0x23u2出错
                            print("<ERROR,INT_UN_DEFINE,LINE "+str(line)+" "+str(flag-befspace)+" >", end=' ')
                            flag += 1
                            flag=skip(prog,flag)
                        else:
                            print("< INT_UN,"+num+" >",end=' ')#
                            flag+=1
                    elif prog[flag].lower()=='l':#同上
                        if prog[flag+1].lower()=='u':
                            if prog[flag + 2].isalnum():
                                print("< ERROR,INT_UN_LONG_DEFINE ,LINE "+str(line)+" "+str(flag-befspace)+" >", end=' ')
                                flag += 3
                                flag = skip(prog, flag)
                            else:
                                print("< INT_UN_LONG,"+num+" >",end=' ')
                                flag+=2
                        elif prog[flag+1].isalnum():
                            print("< ERROR,INT_LONG_DEFINE,LINE "+str(line)+str(flag-befspace)+" >", end=' ')
                            flag += 1
                            flag = skip(prog, flag)
                        else:
                            print("< INT_LONG,"+num+" >",end=' ')
                            flag+=1
                    elif prog[flag].isalpha():#十六进制后接字符则报错
                        print("< ERROR,INT_DEFINE,LINE "+str(line)+" "+str(flag-befspace)+" >",end=' ')
                        flag+=1
                        flag = skip(prog, flag)
                    else:
                        print("< INT," + num + " >", end=' ')
                    pass
                elif prog[flag+1]=='.':#0.开头为浮点数
                    tmp=flag
                    flag+=2
                    haspro=False#是否有+、-、e
                    hasneg=False
                    haseE=False
                    while prog[flag].isdigit() or prog[flag].lower()=='e' or prog[flag]=='-' or prog[flag]=='+':
                        if (prog[flag]=='+' or prog[flag]=='-') and not haseE:break#需满足一些条件
                        elif (prog[flag] == '+' or prog[flag] == '-') and (haspro or hasneg):break
                        elif (prog[flag]=='+' or prog[flag]=='-') and haseE:
                            if prog[flag-1].lower()!='e':break
                            else:
                                if prog[flag]=='+':haspro=True
                                else:hasneg=True
                        elif prog[flag].lower()=='e' and haseE:break
                        elif prog[flag]=='+':haspro=True
                        elif prog[flag] =='-':hasneg = True
                        elif prog[flag].lower()=='e':haseE=True
                        flag+=1
                    befpron=str(reduce(lambda x,y:x+y,prog[tmp:flag]))#拼接
                    findpro=befpron.find('+')
                    findneg=befpron.find('-')
                    findeE=befpron.lower().find('e')
                    IsFLOAT=False
                    IsERROR=False
                    theskip=flag
                    if prog[flag].lower()=='f':#0.23e+002f浮点数声明判断
                        if prog[flag+1].isalnum():#0.23e+002f3报错
                            print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag+1- befspace) + " >",
                                  end=' ')
                            IsERROR=True
                            flag = skip(prog, flag+2)
                        else:
                            IsFLOAT=True
                            theskip=flag+1
                    elif prog[flag].isalnum():#同上
                        print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag-befspace) + " >",
                              end=' ')
                        IsERROR = True
                        flag = skip(prog, flag+1)
                    if not IsERROR:
                        if (hasneg or haspro) and haseE:#有符号指数型
                            pos=(findpro if haspro>hasneg else findneg)
                            if pos!=flag-tmp-1:#处理e+23
                                suffix=int(reduce(lambda x,y:str(int(x)*10+int(y)),befpron[pos+1:]))
                                suffix=suffix if haspro else -suffix
                                num=str(float(str(reduce(lambda x,y:x+y,befpron[0:findeE])))*10**suffix)
                                if IsFLOAT:
                                    print("< FLOAT," + num + " >", end=' ')
                                    flag=theskip
                                else:print("< DOUBLE," + num + " >", end=' ')
                            else:#0.12e+报错
                                print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag - befspace) + " >",
                                      end=' ')
                                flag = skip(prog, flag)
                        elif haseE and not (haspro or hasneg):#无符号指数e
                            if findeE!=flag-tmp-1:
                                suffix = int(str(reduce(lambda x, y: x + y, befpron[findeE+1:])))
                                num = str(float(str(reduce(lambda x, y: x + y, befpron[0:findeE])))
                                          * 10 ** suffix)
                                if IsFLOAT:
                                    print("< FLOAT," + num + " >", end=' ')
                                    flag=theskip
                                else:print("< DOUBLE," + num + " >", end=' ')
                            else:
                                print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag - befspace) + " >",
                                      end=' ')
                                flag = skip(prog, flag)
                            pass
                        else:#单纯的浮点数0.23
                            num=str(float(befpron))
                            if IsFLOAT:
                                print("< FLOAT," + num + " >", end=' ')
                                flag = theskip
                            else:
                                print("< DOUBLE," + num + " >", end=' ')
                elif prog[flag+1].isdigit():#浮点数和八进制均有可能
                    tmp=flag
                    flag+=2
                    haspoint=False#是否有小数点、符号、指数
                    haseE=False
                    haspro=False
                    hasneg=False
                    while prog[flag].isdigit() or prog[flag].lower()=='e' or prog[flag]=='-' or prog[flag]=='+' or prog[flag]=='.':
                        if (prog[flag]=='+' or prog[flag]=='-') and not haseE:break#需满足的一些条件
                        elif (prog[flag] == '+' or prog[flag] == '-') and (haspro or hasneg):
                            break
                        elif (prog[flag]=='+' or prog[flag]=='-') and haseE:
                            if prog[flag-1].lower()!='e':break
                            else:
                                if prog[flag]=='+':haspro=True
                                else:hasneg=True
                        elif (haseE or haspoint) and prog[flag]=='.':break
                        elif prog[flag].lower() == 'e' and haseE:break
                        elif prog[flag]=='.' and haspoint:break

                        elif prog[flag] == '+' :haspro = True
                        elif prog[flag] == '-':hasneg = True
                        elif prog[flag].lower() == 'e' :haseE = True
                        elif prog[flag]=='.' :haspoint=True
                        flag+=1
                    befpron = str(reduce(lambda x, y: x + y, prog[tmp:flag]))#拼接
                    findpro = befpron.find('+')
                    findneg = befpron.find('-')
                    findeE = befpron.lower().find('e')
                    findpoint = befpron.find('.')
                    IsFLOAT = False
                    IsERROR = False
                    theskip = flag
                    if (haspoint or haseE) and prog[flag].lower() == 'f':#同上
                        if prog[flag + 1].isalnum():
                            print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag + 1 - befspace) + " >",
                                  end=' ')
                            IsERROR = True
                            flag = skip(prog, flag + 2)
                        else:
                            IsFLOAT = True
                            theskip = flag + 1
                    elif prog[flag].isalnum():
                        print("< ERROR,NUM_DEFINE,LINE " + str(line) + " " + str(flag - befspace) + " >",
                              end=' ')
                        IsERROR = True
                        flag = skip(prog, flag + 1)
                    if not IsERROR:
                        if haseE and (haspro or hasneg):
                            pos = (findpro if haspro > hasneg else findneg)
                            if pos != flag - tmp - 1:  # 处理e+23
                                suffix = int(reduce(lambda x, y: str(int(x) * 10 + int(y)), befpron[pos + 1:]))
                                suffix = suffix if haspro else -suffix
                                num = str(float(str(reduce(lambda x, y: x + y, befpron[0:findeE]))) * 10 ** suffix)
                                if IsFLOAT:
                                    print("< FLOAT," + num + " >", end=' ')
                                    flag=theskip
                                else:print("< DOUBLE," + num + " >", end=' ')
                            else:  # 0.12e+报错
                                print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag - befspace) + " >",
                                      end=' ')
                                flag = skip(prog, flag)
                        elif haseE :
                            if haseE!=flag-tmp-1:
                                suffix = int(str(reduce(lambda x, y: x + y, befpron[findeE + 1:])))
                                num=str(float(str(reduce(lambda x, y: x + y, befpron[0:findeE])))*10**suffix)
                                if IsFLOAT:
                                    print("< FLOAT," + num + " >", end=' ')
                                    flag=theskip
                                else:print("< DOUBLE," + num + " >", end=' ')
                            else:
                                print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag - befspace) + " >",
                                      end=' ')
                                flag = skip(prog, flag)
                        elif haspoint:
                            if IsFLOAT:
                                print("< FLOAT," + str(float(befpron)) + " >", end=' ')
                                flag = theskip
                            else:
                                print("< DOUBLE," + str(float(befpron)) + " >", end=' ')
                        else:
                            isoctal=True
                            for char in befpron:
                                if int(char)>=8:isoctal=False
                            if not isoctal:
                                print("< ERROR,OCTAL_OUTOFRANG,LINE"+str(line)+" "+str(flag-befspace)+" >",end=' ')
                            else:
                                print("< INT,"+str(int(befpron,8))+">" ,end=' ')
                elif prog[flag+1] in operetor or prog[flag+1] in delimiter:#简单的0
                    print("< INT,0 >",end=' ')
                    flag+=1
                else:#其他字母或符号抛异常
                    flag+=2
                    print("< ERROR,NUM_DEFINE,LINE"+str(line)+" "+str(flag-befspace)+" >",end=' ')
            else:#非0开头可为浮点数或整数
                haspoint=False#同上
                haseE=False
                haspro = False
                hasneg = False
                tmp=flag
                while prog[flag].isdigit() or prog[flag].lower() == 'e' or prog[flag] == '-' or prog[flag] == '+' or \
                                prog[flag] == '.':
                    if (prog[flag] == '+' or prog[flag] == '-') and not haseE:break
                    elif (prog[flag] == '+' or prog[flag] == '-') and (haspro or hasneg):break
                    elif (prog[flag] == '+' or prog[flag] == '-') and haseE:
                        if prog[flag - 1].lower() != 'e':
                            break
                        else:
                            if prog[flag] == '+':
                                haspro = True
                            else:
                                hasneg = True
                    elif (haseE or haspoint) and prog[flag] == '.':break
                    elif prog[flag].lower() == 'e' and haseE:break
                    elif prog[flag] == '.' and haspoint:break
                    elif prog[flag] == '+':
                        haspro = True
                    elif prog[flag] == '-':
                        hasneg = True
                    elif prog[flag].lower() == 'e':
                        haseE = True
                    elif prog[flag] == '.':
                        haspoint = True
                    flag += 1
                befpron = str(reduce(lambda x, y: x + y, prog[tmp:flag]))
                findpro = befpron.find('+')
                findneg = befpron.find('-')
                findeE = befpron.lower().find('e')
                findpoint = befpron.find('.')
                IsFLOAT = False
                IsERROR = False
                theskip = flag
                if (haspoint or haseE) and prog[flag].lower() == 'f':
                    if prog[flag + 1].isalnum():
                        print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag + 1 - befspace) + " >",
                              end=' ')
                        IsERROR = True
                        flag = skip(prog, flag + 2)
                    else:
                        IsFLOAT = True
                        theskip = flag + 1
                elif prog[flag].isalnum():
                    print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag - befspace) + " >",
                          end=' ')
                    IsERROR = True
                    flag = skip(prog, flag + 1)
                if not IsERROR:
                    if haseE and (haspro or hasneg):#有符号指数型
                        pos = (findpro if haspro > hasneg else findneg)
                        if pos != flag - tmp - 1:  # 处理e+23
                            suffix = int(reduce(lambda x, y: str(int(x) * 10 + int(y)), befpron[pos + 1:]))
                            suffix = suffix if haspro else -suffix
                            num = str(float(str(reduce(lambda x, y: x + y, befpron[0:findeE]))) * 10 ** suffix)
                            if IsFLOAT:
                                print("< FLOAT," + num + " >", end=' ')
                                flag = theskip
                            else:
                                print("< DOUBLE," + num + " >", end=' ')
                        else:  # 0.12e+报错
                            print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag - befspace) + " >",
                                  end=' ')
                            flag = skip(prog, flag)
                    elif haseE :#指数型浮点数
                        if haseE != flag - tmp - 1:
                            suffix = int(str(reduce(lambda x, y: x + y, befpron[findeE + 1:])))
                            num = str(float(str(reduce(lambda x, y: x + y, befpron[0:findeE]))) * 10 ** suffix)
                            if IsFLOAT:
                                print("< FLOAT," + num + " >", end=' ')
                                flag = theskip
                            else:
                                print("< DOUBLE," + num + " >", end=' ')
                        else:
                            print("< ERROR,FLOAT_DEFINE,LINE " + str(line) + " " + str(flag - befspace) + " >",
                                  end=' ')
                            flag = skip(prog, flag)
                    elif haspoint:#小数点浮点数
                        if IsFLOAT:
                            print("< FLOAT," + str(float(befpron)) + " >", end=' ')
                            flag = theskip
                        else:
                            print("< DOUBLE," + str(float(befpron)) + " >", end=' ')
                    else:#纯整数
                        num = str(int(befpron))
                        if prog[flag].lower() == 'u':
                            if prog[flag + 1].lower() == 'l':
                                if prog[flag + 2].isalnum():
                                    print("<ERROR,INT_UN_LONG_DEFINE,LINE"+str(line)+" "+str(flag-befspace)+" >", end=' ')
                                    flag += 3
                                    flag = skip(prog, flag)
                                else:
                                    print("<INT_UN_LONG," + num + ">", end=' ')
                                    flag += 2
                            elif prog[flag + 1].isalnum():
                                print("< ERROR,INT_LONG_DEFINE ,LINE"+str(line)+" "+str(flag-befspace)+" >", end=' ')
                                flag += 1
                                flag = skip(prog, flag)
                            else:
                                print("<INT_UN," + num + ">", end=' ')
                        elif prog[flag].lower() == 'l':
                            if prog[flag + 1].lower() == 'u':
                                if prog[flag + 2].isalnum():
                                    print("< ERROR,INT_UN_LONG_DEFINE ,LINE"+str(line)+" "+str(flag-befspace)+" >", end=' ')
                                    flag += 3
                                    flag = skip(prog, flag)
                                else:
                                    print("< INT_UN_LONG," + num + ">", end=' ')
                                    flag += 2
                            elif prog[flag + 1].isalnum():
                                print("< ERROR,INT_LONG_DEFINE ,LINE"+str(line)+" "+str(flag-befspace)+" >", end=' ')
                                flag += 1
                                flag = skip(prog, flag)
                            else:
                                print("< INT_LONG," + num + " >", end=' ')
                        elif prog[flag].isalpha():
                            print("< ERROR,INT_DEFINE,LINE"+str(line)+" "+str(flag-befspace)+" >", end=' ')
                            flag = skip(prog, flag)
                        else:
                            print("< INT," + num + " >", end=' ')
        elif prog[flag] == '\'':#字符
            if prog[flag + 1] != '\\':
                if prog[flag + 1] == '\'':
                    if prog[flag + 2].isalnum():
                        print("< ERROR,CHAR_DEFIEND ,LINE"+str(line)+" "+str(flag-befspace)+" >", end=' ')
                        flag += 3
                        flag = skip(prog, flag)
                    else:
                        print("< CHAR,'' >", end=' ')
                        flag += 2
                elif prog[flag + 2] != '\'':
                    print("< ERROR_MULTI,CHAR_DEFIEND ,LINE"+str(line)+" "+str(flag-befspace)+" >", end=' ')
                    flag += 3
                    while isdeli(prog[flag]) or prog[flag]=='\'':
                        flag += 1
                else:
                    print("< CHAR,'" + prog[flag + 1] + "' >", end=' ')
                    flag+=3
            else:
                if flag + 3 < length and prog[flag + 3] == '\'':
                    print("< CHAR,'" + prog[flag + 1] + prog[flag + 2] + "' >", end=' ')
                    flag += 4
                elif flag + 3 >= length:
                    pass
                else:
                    print("< ERROR_MULTI,CHAR_DEFIEND ,LINE"+str(line)+" "+str(flag-befspace)+" >", end=' ')
                    flag += 3
                    flag = skip(prog, flag)
        elif prog[flag]=='"':#字符串
            flag+=1
            tmp = flag
            while flag<length and not prog[flag]=='"':
                if prog[flag]=='\n':
                    befspace=flag
                    line+=1
                flag+=1
            if flag<length:
                flag+=1
                print('< STRING,"'+str(reduce(lambda x,y:x+y,prog[tmp:flag]))+'" >',end=' ')
            else:
                print("< ERROR,NOMATCH\",LINE " + str(line) + " " + str(flag - befspace) + " >",end=' ')

        elif prog[flag] in delimiter or prog[flag] == ':' or prog[flag] == '?' or prog[flag] == '~':
            #判断不需要分情况的分隔符和操作符
            if prog[flag]!='\\':
                print("< "+prog[flag]+",- >" ,end=' ')
                flag+=1
            else:
                pass
        elif prog[flag] in operetor :
            if prog[flag] == '*':#分情况 乘 指针 乘赋值
                if prog[flag+1]=='=':
                    print("< *=,- >",end=' ')
                    flag+=2
                elif next(prog,flag,False)=='IDENTIFY':
                    print("< *,POINTER OR MUL >",end=' ')
                    flag+=1
                else:
                    print("< *,MUL >",end=' ')
                    flag+=1
                pass
            elif prog[flag] == '/':#除 除赋值 单双行注释
                if prog[flag + 1] == '/':
                    print("< //,ignore >", end=' ')
                    flag+=2
                    while prog[flag]!='\n':
                        flag+=1
                elif prog[flag + 1] == '=':
                    print("< /=,- >", end=' ')
                    flag += 2
                elif prog[flag + 1] == '*':
                    flag+=2
                    ismatch=False
                    while flag+1<length and not (prog[flag]=='*' and prog[flag+1]=='/'):
                        if prog[flag]=='\n':
                            befspace=flag
                            line+=1
                        flag+=1
                    if flag+1<length:
                        flag+=2
                        print("< /**/,ignore >", end=' ')
                    else:
                        print("< ERROR,NOMATCH/*,LINE "+str(line)+" "+str(flag-befspace)+" >")
                else:
                    print("< /,- >", end=' ')
                    flag += 1
            elif prog[flag] == '-':#自减 减赋值 指针 减
                if prog[flag + 1] == '-':
                    print("< --,- >", end=' ')
                    flag += 2
                elif prog[flag + 1] == '=':
                    print("< -=,- >", end=' ')
                    flag += 2
                elif prog[flag + 1] == '>':
                    print("< ->,- >", end=' ')
                    flag += 2
                else:
                    print("< -,- >", end=' ')
                    flag += 1
                pass
            elif prog[flag] == '+':#自增 加赋值 加
                if prog[flag + 1] == '+':
                    print("< ++,- >", end=' ')
                    flag += 2
                elif prog[flag + 1] == '=':
                    print("< +=,- >", end=' ')
                    flag += 2
                else:
                    print("< +,- >", end=' ')
                    flag += 1
                pass
            elif prog[flag] == '%':#求余 求余赋值
                if prog[flag + 1] == '=':
                    print("< %=,- >", end=' ')
                    flag += 2
                else:
                    print("< %,- >", end=' ')
                    flag += 1
                pass
            elif prog[flag] == '=':#等于判断 赋值
                if prog[flag + 1] == '=':
                    print("< ==,- >", end=' ')
                    flag += 2
                else:
                    print("< =.- >", end=' ')
                    flag += 1
                pass
            elif prog[flag] == '>':#右移 右移赋值 大于 大于等于
                if prog[flag + 1] == '>':
                    if prog[flag + 2] == '=':
                        print("< >>=,- >", end=' ')
                        flag += 3
                    else:
                        print("< >>,- >", end=' ')
                        flag += 2
                elif prog[flag + 1] == '=':
                    print("< >=,- >", end=' ')
                    flag += 2
                else:
                    print("< >,- >", end=' ')
                    flag += 1
                pass
            elif prog[flag] == '<':#左移 左移赋值 小于 小于等于
                if prog[flag + 1] == '<':
                    if prog[flag + 2] == '=':
                        print("< <<=,- >", end=' ')
                        flag += 3
                    else:
                        print("< <<,- >", end=' ')
                        flag += 2
                elif prog[flag + 1] == '=':
                    print("< <=,- >", end=' ')
                    flag += 2
                else:
                    print("< <,- >", end=' ')
                    flag+=1
                pass
            elif prog[flag] == '&':#按位与 按位与赋值 逻辑与 取址
                if prog[flag + 1] == '&':
                    print("< &&,- >", end=' ')
                    flag += 2
                elif prog[flag + 1] == '=':
                    print("< &=,- >", end=' ')
                    flag += 2
                elif next(prog,flag,False)=='IDENTIFY':
                    print("< &,Address OR AND >", end=' ')
                    flag += 1
                else:
                    print("< &,- >", end=' ')
                    flag += 1
            elif prog[flag] == '!':#按位与 按位与赋值 逻辑与 取址
                if prog[flag + 1] == '=':
                    print("< !=,- >", end=' ')
                    flag += 2
                else:
                    print("< !,- >", end=' ')
                    flag += 1
            elif prog[flag] == '|':#按位或 按位或赋值 逻辑或
                if prog[flag + 1] == '|':
                    print("< ||,- >", end=' ')
                    flag += 2
                elif prog[flag + 1] == '=':
                    print("< |=,- >", end=' ')
                    flag += 2
                else:
                    print("< |,- >", end=' ')
                    flag += 1
            elif prog[flag] == '^':#按位异或 按位异或赋值
                if prog[flag + 1] == '=':
                    print("< ^=,- >", end=' ')
                    flag += 1
                else:
                    print("< ^,- >", end=' ')
                    flag += 1
                pass
            elif prog[flag] == '.':
                print("< .,- >",end=' ')
                flag+=1
        else :
            print("< ERROR,UNDEFIEND " + prog[flag] + " ,LINE "+str(line)
                  +" "+str(flag-befspace)+">", end=' ')#不可识别的符号
            flag += 1
            flag=skip(prog,flag)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        filename = input("请输入需要分析的文件名：")
        #python3 analyzer
        reader(filename)
    elif sys.argv[1] == '-d':
        #python3 analyzer -d
        #进入测试模式
        test = input("请输入需要测试字符串(回车开始#结束)：")
        while test != "#":
            print("结果为：", end=' ')
            analyse(test+'\n')
            test = input("请输入需要测试字符串(回车开始#结束)：")
    else:
        # python3 analyzer filename分析文件
        reader(sys.argv[1])
    os._exit(0)