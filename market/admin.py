from django.contrib import admin

from .models import User
from .models import Message
from .models import Category
from .models import Trade
from .models import Comment
from .models import TradeReport
from .models import CommentReport
from .models import Chat

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Category)
admin.site.register(Trade)
admin.site.register(Comment)
admin.site.register(TradeReport)
admin.site.register(CommentReport)
admin.site.register(Chat)
