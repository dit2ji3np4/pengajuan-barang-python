from django.contrib import admin
from pengajuan.models import *

admin.site.site_header = "BANK BJB"

class PengajuanAdmin(admin.ModelAdmin):
	list_display=('nama_barang','nomor_memo','tanggal_memo','landasan_kebutuhan','gambar','harga_barang')
	list_filter =['perihal_memo']
class TerimaAdmin(admin.ModelAdmin):
	list_display=('nama_pemilik','divisi','merk','nomor_barang','tanggal_terima','tipe')
	list_filter =['pengajuans']


admin.site.register(Pengajuan,PengajuanAdmin)
admin.site.register(Terima, TerimaAdmin)