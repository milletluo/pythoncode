#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# author: milletluo
# 自动登录邮箱，下载包含关键字和指定日期后的邮件附件
import poplib
import cStringIO
import email
import datetime
import time
from email.header import decode_header

#邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

#下载邮件附件
def GetmailAttachment(emailhost,emailuser,emailpass,datestr,keywords,emailnum):
    host = emailhost
    username = emailuser
    password = emailpass
    keywords = keywords   #查询的邮件的关键字
    datestr = datestr     #查询的邮件日期


    #for 163mail，user POP3 ########
    # pop_conn = poplib.POP3(host)
    #需要验证的邮件服务
    pop_conn = poplib.POP3_SSL(host)
	# 可以打开或关闭调试信息:
    pop_conn.set_debuglevel(1)
    pop_conn.user(username)
    pop_conn.pass_(password)
	# stat()返回邮件数量和占用空间:
    print('Messages: %s. Size: %s' % pop_conn.stat())
    num = len(pop_conn.list()[1])  #邮件总数
    if num < emailnum:  #当总邮件数目小于emailnum的时候读取所有邮件
        num2 = 0
    else:
        num2 = num-emailnum

    getfilesucess = 0
    #遍历倒数emailnum封邮件
    for i in range(num,num2,-1):
		#poplib.rert('邮件号码')方法返回一个元组:(状态信息,邮件,邮件尺寸)
		#hdr,message,octet=server.retr(1) 读去第一个邮件信息.
		#hdr的内容就是响应信息和邮件大小比如'+OK 12498 octets'
		#message 是包含邮件所有行的列表.
		#octet 是这个邮件的内容.
        m = pop_conn.retr(i)
        buf = cStringIO.StringIO()
        #将j存入buf
        for j in m[1]:
            print >> buf,j
        #从buf开头开始算起
        buf.seek(0)
		#Return a message object structure tree from an open file object. This is exactly equivalent to Parser().parse(fp)
        msg = email.message_from_file(buf)
        subject = msg.get("Subject")
        date1 = time.strptime(msg.get("Date")[0:24],'%a, %d %b %Y %H:%M:%S') #格式化收件时间
        date2 = time.strftime("%Y%m%d", date1)
        print(date2)
        #中文邮件的标题和内容都是base64编码的.解码可以使用email.Header 里的decode_header()方法
        subjectnew = decode_str(subject)
        print(subjectnew)
        print(keywords)
        print( "=======================================")
        if (date2>=datestr) and (keywords in subjectnew):
            for part in msg.walk():
                filename = part.get_filename()
                contentType = part.get_content_type()
                mycode=part.get_content_charset();
                print(filename)
                print(contentType)
                print( "---------------------------------------")
                #不知为何excel附件格式为application/octet-stream
                if filename: #and (contentType == 'application/vnd.ms-excel' or contentType == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
                    data = part.get_payload(decode=True)
                    h = email.Header.Header(filename)
                    dh = decode_header(h)
                    fname = dh[0][0]
                    encodeStr = dh[0][1]
                    if encodeStr != None:
                        fname = fname.decode(encodeStr, mycode)

                    fEx = open("%s.%s"%(date2,fname), 'wb')
                    fEx.write(data)
                    fEx.close()
                    print '文件下载成功'
                    getfilesucess += 1

                else:
                    pass
    if getfilesucess == 0:
        print '未找到符合条件的邮件'

    pop_conn.quit()

mail=GetmailAttachment('pop-mail.outlook.com','lm409@hotmail.com','***','20170319',u'test',5)
