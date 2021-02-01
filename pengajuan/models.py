from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django_middleware_global_request.middleware import get_request

class Pengajuan(models.Model):
    nik = models.CharField(max_length=50, null=True)
    nama_barang = models.CharField(max_length=50)
    group_id = models.CharField(max_length=150)
    spesifikasi = models.TextField(max_length=350)
    jumlah = models.IntegerField(default=0,blank=True,null=True)
    receive_quantity = models.IntegerField(default=0, blank=True , null=True)
    receive_by = models.CharField(max_length=50, blank=True , null=True)
    issue_quantity = models.IntegerField(default=0, blank=True , null=True)
    issue_by = models.CharField(max_length=50, blank=True , null=True)
    issue_to = models.CharField(max_length=50,blank=True , null=True)
    landasan_kebutuhan = models.TextField(max_length=350)
    gambar = models.ImageField(upload_to='gambar/' , null=True)
    nomor_memo   = models.CharField(max_length=20)
    tanggal_memo = models.DateField(null=True)
    perihal_memo = models.CharField(max_length=250)
    harga_barang = models.PositiveIntegerField(null=True)
    status = models.IntegerField(default=0, null=True)
    jumlah2 = models.IntegerField(default=0, null=True)
    tl = models.IntegerField(default=0, null=True)
    htl = models.IntegerField(default=0, null=True)
    jumlah3 = models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.nomor_memo

class Terima(models.Model):
    
    nama_pemilik = models.CharField(max_length=60)
    divisi = models.CharField(max_length=80)
    merk = models.CharField(max_length=150)
    jabatan = models.CharField(max_length=150)
    nomor_barang = models.CharField(max_length=90, null=True)
    tanggal_terima = models.DateField(null=True)
    tipe = models.CharField(max_length=150)
    nama_penyerah = models.CharField(max_length=90)
    pemimpin_user = models.CharField(max_length=80)
    pemimpin_pgo = models.CharField(max_length=85)
    pengajuans = models.ForeignKey(Pengajuan, on_delete=models.CASCADE, null=True)












