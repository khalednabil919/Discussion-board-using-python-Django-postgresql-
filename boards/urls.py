from boards import views
from django.contrib import admin
from django.urls import path
 
urlpatterns = [
    #functional based view(FBV)
    # path('',views.home,name='index'),
    path('',views.Home.as_view(),name='index'),
    path('board/<int:board_id>/<int:topic_id>',views.board_topics,name="board_topics"),
    path('board/<int:board_id>/new/',views.new_topic,name='new_topic'),
    path('board/<int:board_id>/topics/<int:topic_id>',views.topic_posts,name="topic_posts"),
    path('board/<int:board_id>/topics/<int:topic_id>/posts/<int:post_id>/edit/',views.PostUpdateView.as_view(),name="edit_post"),
    path('board/<int:board_id>/topics/<int:topic_id>/reply',views.reply_topic,name="reply_topic"),
    #class based view(CBV)
    path('board/<int:board_id>/topics/<int:topic_id>/reply',views.Reply_Topic_CBV.as_view(),name="reply_topic_cbv"),
    #generic class based view(gcbv)
    path('board/<int:board_id>/topics/<int:topic_id>/reply',views.Reply_Topic_GCBV.as_view(),name="reply_topic_gcbv"),
    


]
