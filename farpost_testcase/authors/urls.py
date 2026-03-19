from django.urls import path
from .views import CommentsView, GeneralView

urlpatterns = [
    path('comments/', CommentsView.as_view(), name='comments'),
    path('general/', GeneralView.as_view(), name='general'),
]