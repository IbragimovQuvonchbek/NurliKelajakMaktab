from logging import fatal

from django.db import models


class Tests(models.Model):
    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"

    test_name = models.CharField(verbose_name="Test nomi", max_length=255, blank=False, null=False)
    answers = models.TextField(verbose_name="Javoblar", blank=False, null=False)
    question_quantity = models.SmallIntegerField(verbose_name="Savollar soni", blank=False, null=False, default=20)

    def __str__(self):
        return self.test_name


class Results(models.Model):
    class Meta:
        verbose_name = "Natija"
        verbose_name_plural = "Natijalar"

    name = models.CharField(verbose_name="Ism Familiya", max_length=255, blank=False, null=False)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE, verbose_name="Test Nomi")
    telegram_id = models.CharField(verbose_name="Telegram Id", max_length=255, blank=False, null=False)
    test_solutions = models.TextField(verbose_name="Javoblar", blank=False, null=False)
    result = models.SmallIntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.name} - {self.test.test_name}"
