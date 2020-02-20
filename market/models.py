from django.utils import timezone
from django.db import models


class User(models.Model) :
    user_password = models.CharField(max_length=100)
    user_email = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=512, null=True)
    def __str__(self) :
        return self.name;

class Chat(models.Model) :
    caller_user = models.ForeignKey(User, related_name='caller_user', on_delete=models.DO_NOTHING )
    callee_user = models.ForeignKey(User, related_name='callee_user', on_delete=models.DO_NOTHING )


class Message(models.Model) :
    chat = models.ForeignKey(Chat, related_name='message_chat', on_delete=models.DO_NOTHING, null=True)
    send_user = models.ForeignKey(User, related_name='send_user', on_delete=models.DO_NOTHING)
    recv_user = models.ForeignKey(User, related_name='recv_user', on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=500)
    pub_datetime = models.DateTimeField('date published')
    def __str__(self) :
        return self.send_user.name+","+self.recv_user.name
    
class Category(models.Model) :
    title = models.CharField(max_length=200)
    def __str__(self) :
        return self.title;
    
class Trade(models.Model) :
    title = models.CharField(max_length=200)
    pub_datetime = models.DateTimeField('date published')
    content = models.CharField(max_length=2048)
    price = models.IntegerField(default=0)
    photo = models.CharField(max_length=512)
    pub_user = models.ForeignKey(User, related_name='trade_pub_user', on_delete=models.DO_NOTHING, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    is_soldout = models.BooleanField(default=False)
    interest_count = models.IntegerField(default=0)
    def __str__(self) :
        return self.title[0:10];
    
class Comment(models.Model):
    content = models.CharField(max_length=500)
    pub_datetime = models.DateTimeField('date published')
    pub_user = models.ForeignKey(User, related_name='comment_pub_user', on_delete=models.DO_NOTHING, null=True)
    trade = models.ForeignKey(Trade, on_delete=models.DO_NOTHING)
    def __str__(self) :
        return str(self.pub_user) + " : " + self.content[0:5];

class TradeReport(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.DO_NOTHING)
    pub_report_date = models.DateTimeField('date published', default=timezone.now)
    trade_report_user = models.ForeignKey(User, related_name='trade_report_user', on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=500)
    def __str__(self) :
        return self.trade_report_user.name;

class CommentReport(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)
    pub_report_date = models.DateTimeField('date published')
    comment_report_user = models.ForeignKey(User, related_name='comment_report_user', on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=500)
    def __str__(self) :
        return self.comment_report_user.name + '->'+ self.comment_report_user.name;
        