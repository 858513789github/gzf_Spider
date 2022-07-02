# coding=utf-8
import smtplib
from email.mime.text import MIMEText


def sendmail(subject,receiver,house2email):
    msg = MIMEText(
        '<html><body><h1>有你关注的房源</h1>' + "<p>%s</p>" % house2email + '<p><a href="https://select.pdgzf.com/villageLists">去申请</a></p>' + '</body></html>',
        "html", "utf-8")
    # msg = MIMEText('python email',"plain","utf-8")
    # MIMEText是生成email 的一种格式
    # 参数一:邮件的内容
    # 参数二:邮件的类型
    # 参数三:邮件的编码
    msg['Subject'] = subject  # 邮件的标题
    msg['From'] = "公租房抓取机器人"  # 发件人
    msg['To'] = "主人"  # 收件人

    try:
        # 发送邮件  实例化腾讯的邮件(smtp)服务器
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 设置调试模式
        # server.set_debuglevel(1)
        # 登录实例化的邮件服务器
        server.login("858513789@qq.com", "hmwkopeuduzbbdcj")
        server.sendmail("858513789@qq.com", [receiver], msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    finally:
        server.quit()  # 退出