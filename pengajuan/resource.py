from import_export import resources
from pengajuan.models import Pengajuan
from pengajuan.models import Terima

class PengajuanResource(resources.ModelResource):
    class Meta:
        model = Pengajuan
        exclude = ['id', 'status', 'gambar', 'tl', 'htl', 'receive_quantity', 'receive_by', 'issue_quantity', 'issue_by', 'issue_to', 'jumlah2', 'jumlah3']
        export_order = ['nomor_memo', 'tanggal_memo', 'perihal_memo', 'harga_barang', 'nik', 'group_id', 'nama_barang', 'spesifikasi', 'jumlah', 'landasan_kebutuhan']

class TerimaResource(resources.ModelResource):
    class Meta:
        model = Terima
        exclude = ['nomor_barang']
        export_order = ['nama_pemilik', 'divisi', 'merk', 'jabatan', 'tanggal_terima', 'tipe', 'nama_penyerah', 'pemimpin_user', 'pemimpin_pgo']