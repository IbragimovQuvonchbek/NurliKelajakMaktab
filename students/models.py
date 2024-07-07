from django.db import models


class Talaba(models.Model):
    talaba_ismi = models.CharField(max_length=100, blank=False)
    talaba_familiyasi = models.CharField(max_length=100, blank=False)
    talaba_otasi_nomi = models.CharField(max_length=100, blank=False)
    talaba_yoshi = models.PositiveIntegerField(blank=False)

    otasi_ismi = models.CharField(max_length=100, blank=False)
    otasi_familiyasi = models.CharField(max_length=100, blank=False)
    otasi_otasi_nomi = models.CharField(max_length=100, blank=False)
    otasi_yoshi = models.PositiveIntegerField(blank=False)

    onasi_ismi = models.CharField(max_length=100, blank=False)
    onasi_familiyasi = models.CharField(max_length=100, blank=False)
    onasi_otasi_nomi = models.CharField(max_length=100, blank=False)
    onasi_yoshi = models.PositiveIntegerField(blank=False)

    talaba_telefon_raqami = models.CharField(max_length=100, blank=False)
    otasi_telefon_raqami = models.CharField(max_length=100, blank=False)
    onasi_telefon_raqami = models.CharField(max_length=100, blank=False)

    talaba_yashash_manzili = models.CharField(max_length=1000, blank=False)

    talaba_pasport_id = models.CharField(max_length=100, blank=True)
    talaba_pasport_seriya_raqami = models.CharField(max_length=100, blank=True)

    talaba_fotosurati = models.ImageField(upload_to='talaba_fotosuratlari/', blank=True, null=True)
    talaba_pasport_oldi = models.ImageField(upload_to='talaba_pasport_oldi_suratlari/', blank=True, null=True)
    talaba_pasport_orqa = models.ImageField(upload_to='talaba_pasport_orqa_suratlari/', blank=True, null=True)

    talaba_mavjud = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.talaba_ismi} {self.talaba_familiyasi} {self.talaba_otasi_nomi}"

    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"
