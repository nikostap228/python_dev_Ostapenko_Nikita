from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.utils.dateparse import parse_date
from collections import defaultdict
from authors.models import Author, Post
from logs_app.models import Log, SpaceType, EventType

class CommentsView(APIView):
    """
    Возвращает список комментариев пользователя к постам.
    GET /api/comments/?login=<login>
    """
    def get(self, request):
        login = request.query_params.get('login')
        if not login:
            return Response({"error": "login parameter required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            author = Author.objects.get(login=login)
        except Author.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Получаем тип события "comment" и тип пространства "post" из второй БД
        try:
            comment_event = EventType.objects.using('logs_db').get(name='comment')
            post_space = SpaceType.objects.using('logs_db').get(name='post')
        except (EventType.DoesNotExist, SpaceType.DoesNotExist):
            return Response({"error": "Required event/space types missing in logs DB"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Все комментарии пользователя
        logs = Log.objects.using('logs_db').filter(
            user_id=author.id,
            event_type=comment_event,
            space_type=post_space
        ).exclude(target_id__isnull=True)  # исключаем записи без target_id (поста)

        # Группируем по target_id (post_id) и считаем количество
        post_comments = defaultdict(int)
        for log in logs:
            post_comments[log.target_id] += 1

        # Получаем информацию о постах из первой БД
        post_ids = list(post_comments.keys())
        posts = Post.objects.filter(id__in=post_ids).select_related('author')

        result = []
        for post in posts:
            result.append({
                'login': author.login,
                'post_header': post.header,
                'author_login': post.author.login,
                'comments_count': post_comments[post.id]
            })

        return Response(result)


class GeneralView(APIView):
    """
    Возвращает сводку по действиям пользователя по дням.
    GET /api/general/?login=<login>
    """
    def get(self, request):
        login = request.query_params.get('login')
        if not login:
            return Response({"error": "login parameter required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            author = Author.objects.get(login=login)
        except Author.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Получаем необходимые типы из второй БД
        try:
            login_event = EventType.objects.using('logs_db').get(name='login')
            logout_event = EventType.objects.using('logs_db').get(name='logout')
            blog_space = SpaceType.objects.using('logs_db').get(name='blog')
        except (EventType.DoesNotExist, SpaceType.DoesNotExist):
            return Response({"error": "Required event/space types missing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Все логи пользователя
        logs = Log.objects.using('logs_db').filter(user_id=author.id)

        # Группируем по датам
        daily_stats = defaultdict(lambda: {'login': 0, 'logout': 0, 'blog_actions': 0})

        for log in logs:
            date = log.datetime.date()
            if log.event_type_id == login_event.id:
                daily_stats[date]['login'] += 1
            elif log.event_type_id == logout_event.id:
                daily_stats[date]['logout'] += 1
            if log.space_type_id == blog_space.id:
                daily_stats[date]['blog_actions'] += 1

        # Формируем результат в виде списка, отсортированного по дате
        result = [
            {
                'date': str(date),
                'login_count': stats['login'],
                'logout_count': stats['logout'],
                'blog_actions_count': stats['blog_actions']
            }
            for date, stats in sorted(daily_stats.items())
        ]

        return Response(result)