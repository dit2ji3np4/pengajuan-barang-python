from django.conf import settings
from django.contrib import admin
from django.urls import path
from pengajuan.views  import *
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    #Super Admin
    path('home_superadmin/',home_superadmin, name="home_superadmin"),
    path('alldata/',alldata, name="alldata"),
    path('tambah_pengajuan_superadmin/',tambah_pengajuan_superadmin, name='tambah_pengajuan_superadmin'),
    path('alldata/edit_hapus/<int:id_alldata>',edit_hapus, name="edit_hapus"),
    path('kelolauser/delete_data/<int:id_alldata>', delete_data, name='delete_data'),
    path('kelolauser/',kelolauser, name="kelolauser"),
    path('tambahuser/', tambahuser, name='tambahuser'),
    path('kelolauser/delete_user/<int:id_user>', delete_user, name='delete_user'),
    #Pegawai PGO
    path('home/',home, name="home"),
    path('pengajuan/',allpengajuan ,name='allpengajuan'),
    path('pengajuan/edithapuspgo/<int:id_allpengajuan>',edithapuspgo, name="edithapuspgo"),
    path('pengajuan/deletepgo/<int:id_allpengajuan>', deletepgo, name='deletepgo'),
    path('tambah_pengajuan/',tambah_pengajuan, name='tambah_pengajuan'),
    path('tindaklanjut/',tindaklanjut, name='tindaklanjut'),
    path('hasiltindaklanjut/',hasiltindaklanjut, name="hasiltindaklanjut"),
    path('hasiltindaklanjut/tambahketerangan/<int:id_hasiltindaklanjut>',tambahketerangan, name="tambahketerangan"),
    path('laporan/',laporan, name="laporan"),
    #path('hasiltindaklanjut/tambah_terima/<int:id_hasiltindaklanjut>',tambah_terima, name="tambah_terima"),
    path('tindaklanjut/form/<int:id_tindaklanjut>',form_tindaklanjut, name="form_tindaklanjut"),
    path('tambah_terima/',tambah_terima, name='tambah_terima'),
    path('export/xls/', export_xls, name='export_xls'),
    path('serahterima/', serahterima.as_view(), name="serahterima"),
    path('export/<pk>', terima_render_pdf, name='pdf_render_view'),
    #Pemimpin PGO
    path('home_gh_pgo/', home_gh_pgo, name="home_gh_pgo"),
    path('laporan_all/', laporan_all, name="laporan_all"),
    path('pengajuan_gh_pgo/', pengajuan_gh_pgo, name="pengajuan_gh_pgo"),
    path('hasiltindaklanjut_gh_pgo/', hasiltindaklanjut_gh_pgo, name="hasiltindaklanjut_gh_pgo"),
    path('approve_pgo/<str:id_pengajuan_gh_pgo>', approve_pgo, name="approve_pgo"),
    path('approve_pgo2/<str:id_hasiltindaklanjut_gh_pgo>', approve_pgo2, name="approve_pgo2"),
    path('disapprove_pgo/<str:id_pengajuan_gh_pgo>', disapprove_pgo, name="disapprove_pgo"),
    path('disapprove_pgo2/<str:id_hasiltindaklanjut_gh_pgo>', disapprove_pgo2, name="disapprove_pgo2"),
    #Pegawai Sekum Divisi IT (0)
    path('home0/', home0, name="home0"),
    path('pengajuan0/', pengajuan0, name="pengajuan0"),
    path('pengajuan0/edithapus0/<int:id_pengajuan0>',edithapus0, name="edithapus0"),
    path('pengajuan0/delete0/<int:id_pengajuan0>', delete0, name='delete0'),
    path('tambah_pengajuan_0/',tambah_pengajuan_0, name='tambah_pengajuan_0'),
    path('laporan0/', laporan0, name="laporan0"),
    #Pemimpin Sekum Divisi IT (0)
    path('home_gh_0/', home_gh_0, name="home_gh_0"),
    path('pengajuan_gh_0/', pengajuan_gh_0, name="pengajuan_gh_0"),
    path('approve0/<str:id_pengajuan_gh_0>', approve0, name="approve0"),
    path('disapprove0/<str:id_pengajuan_gh_0>', disapprove0, name="disapprove0"),
    path('laporan_gh_0/', laporan_gh_0, name="laporan_gh_0"),
    #Pegawai Project Management (1)
    path('home1/', home1, name="home1"),
    path('pengajuan1/', pengajuan1, name="pengajuan1"),
    path('pengajuan1/edithapus1/<int:id_pengajuan1>',edithapus1, name="edithapus1"),
    path('pengajuan1/delete1/<int:id_pengajuan1>', delete1, name='delete1'),
    path('tambah_pengajuan_1/',tambah_pengajuan_1, name='tambah_pengajuan_1'),
    path('laporan1/', laporan1, name="laporan1"),
    #Pemimpin Project Management (1)
    path('home_gh_1/', home_gh_1, name="home_gh_1"),
    path('pengajuan_gh_1/', pengajuan_gh_1, name="pengajuan_gh_1"),
    path('approve1/<str:id_pengajuan_gh_1>', approve1, name="approve1"),
    path('disapprove1/<str:id_pengajuan_gh_1>', disapprove1, name="disapprove1"),
    path('laporan_gh_1/', laporan_gh_1, name="laporan_gh_1"),
    #Pegawai Business Intelligence & Analythic (2)
    path('home2/', home2, name="home2"),
    path('pengajuan2/', pengajuan2, name="pengajuan2"),
    path('pengajuan2/edithapus2/<int:id_pengajuan2>',edithapus2, name="edithapus2"),
    path('pengajuan2/delete2/<int:id_pengajuan2>', delete2, name='delete2'),
    path('tambah_pengajuan_2/',tambah_pengajuan_2, name='tambah_pengajuan_2'),
    path('laporan2/', laporan2, name="laporan2"),
    #Pemimpin Business Intelligence & Analythic (2)
    path('home_gh_2/', home_gh_2, name="home_gh_2"),
    path('pengajuan_gh_2/', pengajuan_gh_2, name="pengajuan_gh_2"),
    path('approve2/<str:id_pengajuan_gh_2>', approve2, name="approve2"),
    path('disapprove2/<str:id_pengajuan_gh_2>', disapprove2, name="disapprove2"),
    path('laporan_gh_2/', laporan_gh_2, name="laporan_gh_2"),
    #Pegawai Application Management Core & Non Core (3)
    path('home3/', home3, name="home3"),
    path('pengajuan3/', pengajuan3, name="pengajuan3"),
    path('pengajuan3/edithapus3/<int:id_pengajuan3>',edithapus3, name="edithapus3"),
    path('pengajuan3/delete3/<int:id_pengajuan3>', delete3, name='delete3'),
    path('tambah_pengajuan_3/',tambah_pengajuan_3, name='tambah_pengajuan_3'),
    path('laporan3/', laporan3, name="laporan3"),
    #Pemimpin Application Management Core & Non Core (3)
    path('home_gh_3/', home_gh_3, name="home_gh_3"),
    path('pengajuan_gh_3/', pengajuan_gh_3, name="pengajuan_gh_3"),
    path('approve3/<str:id_pengajuan_gh_3>', approve3, name="approve3"),
    path('disapprove3/<str:id_pengajuan_gh_3>', disapprove3, name="disapprove3"),
    path('laporan_gh_3/', laporan_gh_3, name="laporan_gh_3"),
    #Pegawai Network, Security & Risk Management (4)
    path('home4/', home4, name="home4"),
    path('pengajuan4/', pengajuan4, name="pengajuan4"),
    path('pengajuan4/edithapus4/<int:id_pengajuan4>',edithapus4, name="edithapus4"),
    path('pengajuan4/delete4/<int:id_pengajuan4>', delete4, name='delete4'),
    path('tambah_pengajuan_4/',tambah_pengajuan_4, name='tambah_pengajuan_4'),
    path('laporan4/', laporan4, name="laporan4"),
    #Pemimpin Network, Security & Risk Management (4)
    path('home_gh_4/', home_gh_4, name="home_gh_4"),
    path('pengajuan_gh_4/', pengajuan_gh_4, name="pengajuan_gh_4"),
    path('approve4/<str:id_pengajuan_gh_4>', approve4, name="approve4"),
    path('disapprove4/<str:id_pengajuan_gh_4>', disapprove4, name="disapprove4"),
    path('laporan_gh_4/', laporan_gh_4, name="laporan_gh_4"),
    #Pegawai Operation Management DC & DRC (5)
    path('home5/', home5, name="home5"),
    path('pengajuan5/', pengajuan5, name="pengajuan5"),
    path('pengajuan5/edithapus5/<int:id_pengajuan5>',edithapus5, name="edithapus5"),
    path('pengajuan5/delete5/<int:id_pengajuan5>', delete5, name='delete5'),
    path('tambah_pengajuan_5/',tambah_pengajuan_5, name='tambah_pengajuan_5'),
    path('laporan5/', laporan5, name="laporan5"),
    #Pemimpin Operation Management DC & DRC (5)
    path('home_gh_5/', home_gh_5, name="home_gh_5"),
    path('pengajuan_gh_5/', pengajuan_gh_5, name="pengajuan_gh_5"),
    path('approve5/<str:id_pengajuan_gh_5>', approve5, name="approve5"),
    path('disapprove5/<str:id_pengajuan_gh_5>', disapprove5, name="disapprove5"),
    path('laporan_gh_5/', laporan_gh_5, name="laporan_gh_5"),
    #Pegawai Helpdesk & Support (6)
    path('home6/', home6, name="home6"),
    path('pengajuan6/', pengajuan6, name="pengajuan6"),
    path('pengajuan6/edithapus6/<int:id_pengajuan6>',edithapus6, name="edithapus6"),
    path('pengajuan6/delete6/<int:id_pengajuan6>', delete6, name='delete6'),
    path('tambah_pengajuan_6/',tambah_pengajuan_6, name='tambah_pengajuan_6'),
    path('laporan6/', laporan6, name="laporan6"),
    #Pemimpin Helpdesk & Support (6)
    path('home_gh_6/', home_gh_6, name="home_gh_6"),
    path('pengajuan_gh_6/', pengajuan_gh_6, name="pengajuan_gh_6"),
    path('approve6/<str:id_pengajuan_gh_6>', approve6, name="approve6"),
    path('disapprove6/<str:id_pengajuan_gh_6>', disapprove6, name="disapprove6"),
    path('laporan_gh_6/', laporan_gh_6, name="laporan_gh_6"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)