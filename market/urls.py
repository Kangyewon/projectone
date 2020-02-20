from django.urls import include, path
from . import views


urlpatterns = [
    path('login', views.user_login, name='login'),
    path('login_with_token', views.user_login_with_token, name='login'),
    path('join_membership', views.join_membership, name='join'),
    path('categories', views.categories, name="categories"),
    path('trades', views.trades, name="trades"),
    path('trades/<int:category_id>', views.trades_with_category, name="trades_with_category"),
    path('trade/pub', views.pub_trade, name="pub_trade"),
    path('trades/<int:trade_id>',views.trade, name="trade"),
    path('trades/<int:trade_id>/comments', views.comments, name='comments'),
    path('trades/<int:trade_id>/comment/pub', views.pub_comment, name='pub_comment'),
    path('user/trades',views.user_trades, name="user_trades"),
    path('user/comments',views.user_comments, name="user_comments"),
    path('message', views.message_send, name="message_send"),
    path('chat', views.new_chat, name="new_chat"),
    path('user/my_chats', views.my_chats, name="my_chats"),
    path('trade_report', views.trade_report, name="trade_report"),
    path('comment_report', views.comment_report, name="comment_report"),
    path('withdrawal', views.withdrawal, name="withdrawal"),
    path('user/change_name', views.user_name_change, name="user_name_change"),
    path('trades/<int:trade_id>/change', views.trade_content_change, name="trade_content_change"),
    path('logout', views.logout, name="logout"),
    path('message_receive', views.message_receive, name="message_receive"),
    path('message_re', views.message_receive, name="message_re")
]