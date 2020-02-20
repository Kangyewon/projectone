from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import *
import hashlib
import random

def make_response_with_success(result):
    new_result = {'error_code' : 200, 'error_message' : 'Success'}
    new_result.update(result)
    return JsonResponse(new_result)

def make_response(code, message):
    result = {'error_code' : code, 'error_message' : message}
    return JsonResponse(result)


#수동 로그인
@csrf_exempt
def user_login(request):
    user_id = request.POST['id']
    user_password = request.POST['password']
    
    user = User.objects.get(user_email=user_id)
    if (user.user_password == user_password):
        encoded_str = user.name+str(random.random())
        user.token = hashlib.sha256(encoded_str.encode()).hexdigest()
        user.save()
        result = {'token' : user.token}
        return make_response_with_success(result)
    return make_response(400, 'Invalid user')

#토큰으로 로그인
@csrf_exempt
def user_login_with_token(request):
    user_token = request.POST['token']
    try :
        user = User.objects.get(token = user_token)
    except Exception as ex :
        return make_response(404, 'User is not found')
    return make_response(200, 'Success')



    

#회원가입
@csrf_exempt
def join_membership(request):
    user_id = request.POST['id']
    try:
        user = User.objects.get(user_email=user_id)
        return make_response(401, 'User id is aleady exists')
    except Exception as ex:
        pass
    name = request.POST['name']
    user_password = request.POST['password']
    
    new_user = User()
    new_user.name = name
    new_user.user_email = user_id
    new_user.user_password = user_password
    new_user.save()

    return make_response(200,'Success')

#카테고리 목록
def categories(request) :
    categories = Category.objects.all()
    result_categories = []
    for category in categories :
        result_category = {'id' : category.id, 'title' : category.title}
        result_categories.append(result_category)
    result = {'categories' : result_categories}
    return make_response_with_success(result)

#거래글 목록
def trades(request) :
    trades = Trade.objects.all()
    result_trades = []
    for trade in trades :
        user_name = trade.pub_user != None and trade.pub_user.name or ""
        result_trade = {
            'id' : trade.id, 
            'category' : trade.category.title, 
            'title' : trade.title, 
            'pub_datetime' : trade.pub_datetime,
            'photo' : trade.photo, 
            'price' : trade.price,
            'pub_user' : user_name,
            'interest_count' : trade.interest_count}
        result_trades.append(result_trade)
    result = {'trades' : result_trades}
    return make_response_with_success(result)

#카테고리별 거래글 목록
def trades_with_category(request,category_id) :
    try:
        selected_category = Category.objects.get(pk = category_id)
    except Category.DoesNotExist :
        return make_response(404, 'Category is not found')
    
    trades = Trade.objects.filter(category = selected_category)
    result_trades = []
    for trade in trades :
        result_trade = {
            'id' : trade.id, 
            'category' : trade.category.title, 
            'title' : trade.title, 
            'pub_datetime' : trade.pub_datetime,
            'photo' : trade.photo, 
            'price' : trade.price,
            'pub_user' : trade.pub_user.name,
            'interest_count' : trade.interest_count}
        result_trades.append(result_trade)
    result = {'trades' : result_trades}
    return make_response_with_success(result)

#거래글 상세
def trade(request, trade_id):
    try:
        trade = Trade.objects.get(pk=trade_id)
    except Trade.DoesNotExist:
        return make_response(404, 'Trade is not found')

    result_trade = {
        'id' : trade.id,
        'pub_user' : trade.pub_user.name,
        'pub_user_id' : trade.pub_user.id,
        'category' : trade.category.title, 
        'title' : trade.title,
        'content' : trade.content,
        'pub_datetime' : trade.pub_datetime,
        'photo' : trade.photo, 
        'price' : trade.price, 
        'interest_count' : trade.interest_count,
        'is_soldout' : trade.is_soldout
    }
    return make_response_with_success(result_trade)

#거래글의 댓글 작성
@csrf_exempt
def pub_comment(request, trade_id) :
    post_content = request.POST['content']
    pub_user_token = request.POST['token']
    try:
        trade = Trade.objects.get(pk=trade_id)
    except Trade.DoesNotExist:
        return make_response(404, 'Trade is not found')
    
    try:
        user = User.objects.get(token = pub_user_token)
    except User.DoesNotExist:
        return make_response(404, 'User is not found')
       
    new_comment = trade.comment_set.create(pub_user = user, content = post_content, pub_datetime = timezone.now())
    
    return make_response(200, "Success")

#거래글 등록
@csrf_exempt
def pub_trade(request) :
    pub_user_token = request.POST['token']
    category_id = request.POST['category_id']
    try :
        user = User.objects.get(token = pub_user_token)
    except User.DoesNotExist:
        return make_response(404, 'User is not found')
    try :
        category = Category.objects.get(pk = category_id)
    except Category.DoesNotExist:
        return make_response(404, 'Category is not found')

    new_trade = Trade()
    new_trade.pub_user = user
    new_trade.pub_datetime = timezone.now()
    new_trade.title = request.POST['title']
    new_trade.content = request.POST['content']
    new_trade.price = request.POST['price']
    new_trade.photo = request.POST['photo_url']
    new_trade.category = category
    new_trade.is_soldout = False
    new_trade.interest_count = 0
    new_trade.save()

    return make_response(200, "Success")



#거래글의 댓글 요청(거래글에 대한 댓글보기)
def comments(request, trade_id) :
    try:
        selected_trade = Trade.objects.get(pk=trade_id)
    except Trade.DoesNotExist :
        return make_response(404, 'Trade is not found')

    comments = Comment.objects.filter(trade = selected_trade)
    comments_dict = []
    for comment in comments:
        comment_dict = {}
        comment_dict['id'] = comment.id
        comment_dict['pub_user'] = comment.pub_user.name
        comment_dict['pub_datetime'] = comment.pub_datetime
        comment_dict['content'] = comment.content
        comments_dict.append(comment_dict)
    
    result = {'comments' : comments_dict}

    return make_response_with_success(result)

    result_comment = {
        'id' : comment.id,
        'content' : comment.content,
        'pub_datetime' : comment.pub_datetime,
        'pub_user' : comment.pub_user,
        'trade' : comment.trade
    }
    return make_response_with_success(result_comment)

#사용자 이름 변경
@csrf_exempt
def user_name_change(request) :
    user_token = request.POST['token']
    try :
        user = User.objects.get(token = user_token)
    except User.DoesNotExist :
        return make_response(404, 'User is not found')
    
    user.name = request.POST['user_name']
    user.save()
    
    return make_response(200, "Success")

#로그아웃
@csrf_exempt
def logout(request) :
    user_token = request.POST['token']
    try :
        user = User.objects.get(token = user_token)
    except User.DoesNotExist :
        return make_response(404, 'User is not found')
    
    user.token = ''
    user.save()
    return make_response(200, "Success")

#탈퇴
@csrf_exempt
def withdrawal(request) :
    user = request.POST['token']
    try :
        user = User.objects.get(token = user)
    except User.DoesNotExist :
        return make_response(404, 'User is not found')

    user.delete()
    
    return make_response(200, "Success")

#내 거래글 목록
def user_trades(request) :
    pub_user_token = request.GET['token']
    try :
        user = User.objects.get(token = pub_user_token)
    except User.DoesNotExist :
        return make_response(404, 'User is not found')
    
    trades = Trade.objects.filter(pub_user=user)
    result_trades = []
    for trade in trades :
        result_trade = {
            'id' : trade.id, 
            'category' : trade.category.title, 
            'title' : trade.title, 
            'pub_datetime' : trade.pub_datetime,
            'photo' : trade.photo, 
            'price' : trade.price,
            'pub_user' : trade.pub_user.name,
            'interest_count' : trade.interest_count}
        result_trades.append(result_trade)
    result = {'trades' : result_trades}
    return make_response_with_success(result)

#내 댓글 목록
def user_comments(request) :
    pub_user_token = request.GET['token']
    try :
        user = User.objects.get(token = pub_user_token)
    except User.DoesNotExist :

        return make_response(404, 'User is not found')
    
    comments = Comment.objects.filter(pub_user=user)
    comments_dict = []
    for comment in comments:
        comment_dict = {}
        comment_dict['id'] = comment.id
        comment_dict['pub_user'] = comment.pub_user.name
        comment_dict['pub_datetime'] = comment.pub_datetime
        comment_dict['content'] = comment.content
        comments_dict.append(comment_dict)
    
    result = {'comments' : comments_dict}

    return make_response_with_success(result)

# 대화방 생성
@csrf_exempt
def new_chat(request) :
    caller_user_token = request.POST['token']
    callee_user_id = request.POST['callee_user_id']
    try :
        caller_user = User.objects.get(token = caller_user_token)
    except User.DoesNotExist:
        return make_response(404, 'User is not found')
    try :
        callee_user = User.objects.get(pk = callee_user_id)
    except User.DoesNotExist :
        return make_response(404, 'Callee user is not found')
    
    new_chat = Chat()
    new_chat.caller_user = caller_user
    new_chat.callee_user = callee_user
    new_chat.save()

    result = {'idx':new_chat.id}

    return make_response_with_success(result)

#내 대화방 목록
def my_chats(request) :
    user_token = request.GET['token']
    try :
        user = User.objects.get(token = user_token)
    except User.DoesNotExist :
        return make_response(404, 'User is not found')
        
    chats = Chat.objects.filter(caller_user = user) | Chat.objects.filter(callee_user = user)
    chats_dict = []
    for chat in chats :
        chat_dict = {}
        chat_dict['id'] = chat.id
        chat_dict['caller_user'] = chat.caller_user.name
        chat_dict['callee_user'] = chat.callee_user.name
        chats_dict.append(chat_dict)
    result = {'chats' : chats_dict}
    return make_response_with_success(result)

#대화(보내기)
@csrf_exempt
def message_send(request) :
    send_user_token = request.POST['token']
    recv_user_id = request.POST['recv_user_id']
    chat_id = request.POST['chat_id']
    try :
        send_user = User.objects.get(token = send_user_token)
    except User.DoesNotExist:
        return make_response(404, 'User is not found')
    try :
        recv_user = User.objects.get(pk = recv_user_id)
    except User.DoesNotExist:
        return make_response(404, 'Recv User is not found')
    try :
        chat = Chat.objects.get(pk = chat_id)
    except Chat.DoesNotExist :  
        return make_response(404, 'Chat is not found')

    new_message = Message()
    new_message.chat = chat
    new_message.send_user = send_user
    new_message.recv_user = recv_user
    new_message.content = request.POST['content']
    new_message.pub_datetime = timezone.now()
    new_message.save()
    return make_response(200, "Success")

#대화방 내용 (대화방에서 주고 받은 내용)
def message_receive(request) :
    send_user_token = request.GET['token']
    recv_user_id = request.GET['recv_user_id']
    try :
        send_user = User.objects.get(token = send_user_token)
    except User.DoesNotExist :
        return make_response(404, 'User is not found')

    try :
        recv_user = User.objects.get(pk = recv_user_id)
    except User.DoesNotExist :
        return make_response(404, 'Recv User is not found')

    messages = Message.objects.filter(send_user=send_user)
    messages_dict = []
    
    for message in messages :
        message_dict = {}
        message_dict['id'] = message.id
        message_dict['send_user'] = message.send_user.name
        message_dict['recv_user'] = message.recv_user.name
        message_dict['content'] = message.content
        message_dict['pub_datetime'] = message.pub_datetime
        messages_dict.append(message_dict)
    
    result = {'messages' : messages_dict}

    return make_response_with_success(result)

#댓글신고하기
@csrf_exempt
def comment_report(request) :
    comment_report_user_token = request.POST['token']
    comment_id = request.POST['comment_id']
    try :
        comment_report_user = User.objects.get(token = comment_report_user_token)
    except User.DoesNotExist :
        return make_response(404, 'User is not found')
    try :
        comment = Comment.objects.get(pk = comment_id)
    except Comment.DoesNotExist :
        return make_response(404, 'Comment is not found')
    
    new_comment_report = CommentReport()
    new_comment_report.comment = comment
    new_comment_report.comment_report_user = comment_report_user
    new_comment_report.pub_report_date = timezone.now()
    new_comment_report.content = request.POST['content']
    new_comment_report.save()

    return make_response(200, "Success")
    
#거래글신고하기
@csrf_exempt
def trade_report(request) :
    trade_report_user_token = request.POST['token']
    trade_id = request.POST['trade_id']
    try :
        trade_report_user = User.objects.get(token = trade_report_user_token)
    except User.DoesNotExist :
        return make_response(404, 'User is not found')
    try :
        trade = Trade.objects.get(pk = trade_id)
    except Trade.DoesNotExist :
        return make_response(404, 'Trade is not found')
    
    new_trade_report = TradeReport()
    new_trade_report.trade = trade
    new_trade_report.trade_report_user = trade_report_user
    new_trade_report.pub_report_date = timezone.now()
    new_trade_report.content = request.POST['content']
    new_trade_report.save()

    return make_response(200, "Success")

#거래글 수정하기
@csrf_exempt
def trade_content_change(request, trade_id) :
    user_token = request.POST['token']
    category_id = request.POST['category_id']
    
    try :
        user = User.objects.get(token = user_token)
    except User.DoesNotExist :
        return make_response(404, 'User is not found')
    try :
        trade = Trade.objects.get(pk = trade_id)
    except Trade.DoesNotExist :
        return make_response(404, 'Trade is not found')
    try :
        category = Category.objects.get(pk = category_id)
    except Category.DoesNotExist :
        return make_response(404, 'Category is not found')
    
    if (user != trade.pub_user) :
        return make_response(404, 'Invalid user')

    trade.title = request.POST['title']
    trade.pub_datetime = timezone.now()
    trade.content = request.POST['content']
    trade.price = request.POST['price']
    trade.photo = request.POST['photo_url']
    trade.category = category
    trade.is_soldout = False
    interest_count = 0
    trade.save()

    return make_response(200, "Success")