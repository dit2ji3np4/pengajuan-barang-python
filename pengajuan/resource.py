from import_export import resources
from pengajuan.models import Pengajuan

class PengajuanResource(resources.ModelResource):
    class Meta:
        model = Pengajuan
        exclude = ['id', 'status', 'gambar', 'tl', 'htl']
        export_order = ['nomor_memo', 'tanggal_memo', 'perihal_memo', 'harga_barang', 'nik', 'group_id', 'nama_barang', 'spesifikasi', 'jumlah', 'landasan_kebutuhan']