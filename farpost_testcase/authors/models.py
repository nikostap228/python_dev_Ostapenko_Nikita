from django.db import models

class Author(models.Model):
    login = models.CharField(max_length=100, unique=True)
    email = models.EmailField()

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.login

class Blog(models.Model):
    owner = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blogs')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.name

class Post(models.Model):
    header = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.header