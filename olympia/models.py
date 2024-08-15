from django.db import models


class Olimpiada25082024(models.Model):
    class Meta:
        verbose_name = "Olimpiada 25.08.2024"
        verbose_name_plural = "Olimpiada 25.08.2024"

    name = models.CharField(verbose_name="F.I.Sh", max_length=255, blank=False, null=False)
    grade = models.CharField(verbose_name="Sinf", max_length=255, blank=False, null=False)
    phone = models.CharField(verbose_name="Tel", max_length=255, blank=False, null=False)
    telegram_id = models.CharField(verbose_name="Telegram_id", max_length=255, blank=False, null=False)

    def __str__(self):
        return self.telegram_id
