from django.db import models

# Create your models here.

class Topic(models.Model):
    """Temat poznawany przez użytkownika."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Zwraca reprezentację modelu w postaci ciągu tekstowego"""
        return self.text

class Entry(models.Model):
    """Konkretne informacje o postępie w nauce."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'entries'
        verbose_name_plural = verbose_name

    def __str__(self):
        """Zwraca reprezentację modelu w postaci ciągu tekstowego"""
        return self.text[:50] + "..."
