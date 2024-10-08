from django.db import models
import random
import string
from datetime import datetime


class Student(models.Model):
    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"

    first_name = models.CharField(max_length=255, blank=False, verbose_name="Ism")
    last_name = models.CharField(max_length=255, blank=False, verbose_name="Familiya")
    grade = models.PositiveSmallIntegerField(blank=False, verbose_name="Sinf")
    group = models.PositiveSmallIntegerField(blank=False, default=1, verbose_name="Gruh raqami")
    id_unique = models.CharField(max_length=255, default=lambda : Student.generate_unique_code(),
                                 verbose_name="O'quvchi ID")
    @staticmethod
    def generate_unique_code():
        characters = string.ascii_uppercase + string.digits
        unique_code = ''.join(random.choices(characters, k=6))
        return unique_code

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentResult(models.Model):
    class Meta:
        verbose_name = "Natija"
        verbose_name_plural = "Natijalar"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="O'quvchi")
    number_of_questions = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name="Savollar soni")
    result = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name="Natija")
    month = models.CharField(max_length=100, blank=False, null=False,
                             default=lambda : StudentResult.get_current_month_in_uzbek())

    @staticmethod
    def get_current_month_in_uzbek():
        current_month = datetime.now().month
        months_in_uzbek = {
            1: "Yanvar",
            2: "Fevral",
            3: "Mart",
            4: "Aprel",
            5: "May",
            6: "Iyun",
            7: "Iyul",
            8: "Avgust",
            9: "Sentabr",
            10: "Oktabr",
            11: "Noyabr",
            12: "Dekabr"
        }
        return months_in_uzbek[current_month]

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}  --  {self.number_of_questions}/{self.result}"
