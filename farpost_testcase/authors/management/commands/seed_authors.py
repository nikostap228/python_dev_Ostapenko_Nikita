from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Seed authors, blogs and posts'

    def handle(self, *args, **options):
        Author = apps.get_model('authors', 'Author')
        Blog = apps.get_model('authors', 'Blog')
        Post = apps.get_model('authors', 'Post')

        # Создаём авторов
        author1, _ = Author.objects.get_or_create(login='nikita', email='nikita@example.com')
        author2, _ = Author.objects.get_or_create(login='andrey', email='andrey@example.com')
        author3, _ = Author.objects.get_or_create(login='alexey', email='alexey@example.com')

        # Создаём блоги
        blog1, _ = Blog.objects.get_or_create(owner=author1, name="Nikit's Blog", description="About everything")
        blog2, _ = Blog.objects.get_or_create(owner=author2, name="Andrey's Tech Blog", description="Tech stuff")

        # Создаём посты
        post1, _ = Post.objects.get_or_create(header="First Post", text="Hello world", author=author1, blog=blog1)
        post2, _ = Post.objects.get_or_create(header="Second Post", text="Django tips", author=author1, blog=blog1)
        post3, _ = Post.objects.get_or_create(header="Python vs Java", text="Comparison", author=author2, blog=blog2)

        self.stdout.write("Test data created.")