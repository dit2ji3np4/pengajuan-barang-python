import os
from django.shortcuts import render ,redirect, reverse , get_object_or_404
from django.http import HttpResponse , HttpResponseNotFound
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from pengajuan.resource import PengajuanResource, TerimaResource
from .decorators import allowed_users, pgo_only
from django.db.models import Q
#pdf exsport
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.views.generic  import ListView
#
from io import StringIO
from django.template import Context





#Super User
@login_required
@allowed_users(allowed_roles=['Super Admin'])
def home_superadmin(request):
    permintaandata = Pengajuan.objects.all()
    userdata = User.objects.all()
    return render(request,'home_superadmin.html',{'data' : permintaandata,'user' : userdata})

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def alldata(request):
    data = Pengajuan.objects.all()
    konteks = { 
        'data' : data,
    }
    return render(request,'alldata.html',konteks)

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def tambah_pengajuan_superadmin(request):
    if request.POST:
        form = FormTambahketerangan(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormTambahketerangan()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_pengajuan_superadmin.html',konteks)

    else:
        form = FormTambahketerangan()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_pengajuan_superadmin.html',konteks)

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def edit_hapus(request, id_alldata):
    alldata = Pengajuan.objects.get(id=id_alldata)
    template = 'edit_hapus.html'
    if request.POST:
        form = FormTambahketerangan(request.POST, instance=alldata)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('alldata')
    else:
        form = FormTambahketerangan(instance=alldata)
        konteks = {
            'form':form,
            'alldata':alldata,
        }
    return render(request, template, konteks)

class serahterima2(ListView):
    model = Terima 
    template_name = 'serahterima2.html'

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def tambah_terima2(request):
    if request.POST:
        form = FormTerima(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormTerima()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_terima2.html',konteks)

    else:
        form = FormTerima()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_terima2.html',konteks)

@login_required
def delete_terima(request, id_terima):
    dterima = Terima.objects.filter(id=id_terima)
    dterima.delete()

    return redirect('serahterima2')

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def delete_data(request, id_alldata):
    ddata = Pengajuan.objects.filter(id=id_alldata)
    ddata.delete()

    return redirect('alldata')

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def kelolauser(request ):
    #permintaanuser = Group.objects.get()
    #User = get_user_model()
    user = User.objects.all()
    konteks = { 
        'user' : user,
    }
    return render(request,'kelolauser_pgo.html', konteks)

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def kelolagroup(request ):
    #permintaanuser = Group.objects.get()
    #User = get_user_model()
    group = Group.objects.all()
    konteks = { 
        'group' : group,
    }
    return render(request,'kelolagroup.html', konteks)

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def editgroup(request, id_kelolagroup):
    kelolagroup = Group.objects.get(id=id_kelolagroup)
    template = 'editgroup.html'
    if request.POST:
        form = UserGroupForm(request.POST, instance=kelolagroup)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('kelolagroup')
    else:
        form = UserGroupForm(instance=kelolagroup)
        konteks = {
            'form':form,
            'kelolagroup':kelolagroup,
        }
    return render(request, template, konteks)

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def edituser(request, id_kelolauser):
    kelolauser = User.objects.get(id=id_kelolauser)
    template = 'edituser.html'
    if request.POST:
        form = UserProfileForm(request.POST, instance=kelolauser)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('kelolauser')
    else:
        form = UserProfileForm(instance=kelolauser)
        konteks = {
            'form':form,
            'kelolauser':kelolauser,
        }
    return render(request, template, konteks)

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def delete_user(request, id_user):
    duser = User.objects.filter(id=id_user)
    duser.delete()

    return redirect('kelolauser')

@login_required
@allowed_users(allowed_roles=['Super Admin'])
def tambahuser(request):
    if request.POST:
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(user)
            messages.success(request, "User berhasil ditambah")
            return redirect('tambahuser')
        else:
            messages.error(request, "Error! (Username sudah digunakan / Password tidak sama)")
            return redirect('tambahuser')
    else:
        form = UserProfileForm()
        konteks = {
            'form':form,
        }
    return render(request, 'tambahuser_pgo.html', konteks)

#Bagian Pegawai PGO
@login_required(login_url=settings.LOGIN_URL)
@pgo_only
@allowed_users(allowed_roles=['Planning and Governance'])
def home(request):
    data1 = Pengajuan.objects.filter(status=1).count()
    data2 = Pengajuan.objects.filter(status=3).exclude(jumlah2=0).count()
    return render(request,'home_pgo.html',{'data1' : data1, 'data2' : data2})

@login_required(login_url=settings.LOGIN_URL)
@pgo_only
@allowed_users(allowed_roles=['Planning and Governance'])
def allpengajuan(request):
    permintaan = Pengajuan.objects.filter(group_id='Planning and Governance')
    konteks = { 
        'permintaan' : permintaan,
    }
    return render(request,'pengajuan_pgo.html',konteks)

def edithapuspgo(request, id_allpengajuan):
    allpengajuan = Pengajuan.objects.get(id=id_allpengajuan)
    template = 'edithapuspgo.html'
    if request.POST:
        form = FormPengajuan(request.POST, instance=allpengajuan)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('allpengajuan')
    else:
        form = FormPengajuan(instance=allpengajuan)
        konteks = {
            'form':form,
            'allpengajuan':allpengajuan,
        }
    return render(request, template, konteks)

def deletepgo(request, id_allpengajuan):
    dpgo = Pengajuan.objects.filter(id=id_allpengajuan)
    dpgo.delete()

    return redirect('allpengajuan')

@login_required(login_url=settings.LOGIN_URL)
@pgo_only
@allowed_users(allowed_roles=['Planning and Governance'])
def form_tindaklanjut(request, id_tindaklanjut):
    tindaklanjut = Pengajuan.objects.get(id=id_tindaklanjut)
    template = 'form_tindaklanjut_pgo.html'
    if request.POST:
        form = FormTindaklanjut(request.POST, instance=tindaklanjut)
        if form.is_valid():
            form.save()
            messages.success(request, "Berhasil Disimpan")
            return redirect('tindaklanjut')
    else:
        form = FormTindaklanjut(instance=tindaklanjut)
        konteks = {
            'form':form,
            'tindaklanjut':tindaklanjut,
        }
    return render(request, template, konteks)

@login_required(login_url=settings.LOGIN_URL)
@pgo_only
@allowed_users(allowed_roles=['Planning and Governance'])
def tindaklanjut(request):
    permintaan2 = Pengajuan.objects.filter(tl=1)
    konteks = {
        'permintaan2' : permintaan2,
    }
    return render(request,'tindaklanjut_pgo.html',konteks)


@login_required(login_url=settings.LOGIN_URL)
@pgo_only
@allowed_users(allowed_roles=['Planning and Governance'])
def tambah_pengajuan(request):
    if request.POST:
        form = FormPengajuan(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormPengajuan()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_pengajuan.html',konteks)

    else:
        form = FormPengajuan()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_pengajuan.html',konteks)

@login_required(login_url=settings.LOGIN_URL)
@pgo_only
@allowed_users(allowed_roles=['Planning and Governance'])
def tambahketerangan(request, id_hasiltindaklanjut):
    hasiltindaklanjut = Pengajuan.objects.get(id=id_hasiltindaklanjut)
    template = 'tambahketerangan_pgo.html'
    if request.POST:
        form = FormTambahketerangan(request.POST, instance=hasiltindaklanjut)
        if form.is_valid():
            form.save()
            messages.success(request, "Keterangan Berhasil Disimpan")
            return redirect('hasiltindaklanjut')
    else:
        form = FormTambahketerangan(instance=hasiltindaklanjut)
        konteks = {
            'form':form,
            'hasiltindaklanjut':hasiltindaklanjut,
        }
    return render(request, template, konteks)

@login_required(login_url=settings.LOGIN_URL)
@pgo_only
@allowed_users(allowed_roles=['Planning and Governance'])
def hasiltindaklanjut(request):
    permintaan3 = Pengajuan.objects.filter(status=3)
    konteks = {
        'permintaan3' : permintaan3,
    }
    return render(request,'hasiltindaklanjut_pgo.html',konteks)

@login_required(login_url=settings.LOGIN_URL)
@pgo_only
@allowed_users(allowed_roles=['Planning and Governance'])
def laporan(request):
    permintaan4 = Pengajuan.objects.filter(status=3)
    konteks = {
        'permintaan4' : permintaan4,
    }
    return render(request,'laporan_pgo.html',konteks)

class serahterima(ListView):
    model = Terima 
    template_name = 'serahterima.html'

def edit_hapus_terima(request, id_terima):
    terima = Terima.objects.get(id=id_terima)
    template = 'edit_hapus_terima.html'
    if request.POST:
        form = FormTerima(request.POST, instance=terima)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('serahterima')
    else:
        form = FormTerima(instance=terima)
        konteks = {
            'form':form,
            'terima':terima,
        }
    return render(request, template, konteks)

def delete_terima2(request, id_terima):
    dterima2 = Terima.objects.filter(id=id_terima)
    dterima2.delete()

    return redirect('serahterima')

def tambah_terima(request):
    if request.POST:
        form = FormTerima(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormTerima()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_terima.html',konteks)

    else:
        form = FormTerima()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_terima.html',konteks)
#Bagian Pemimpin PGO

@login_required
@allowed_users(allowed_roles=['GH Planning and Governance'])
def home_gh_pgo(request):
    data6 = Pengajuan.objects.filter(group_id='Planning and Governance', status='0').count()
    dataex = Pengajuan.objects.filter(group_id='Sekum Divisi IT', status='0').count()
    data7 = Pengajuan.objects.filter(status='2').count()
    return render(request,'home_pemimpin_pgo.html',{'data6' : data6, 'data7' : data7, 'dataex' : dataex})

@login_required
@allowed_users(allowed_roles=['GH Planning and Governance'])
def laporan_all(request):
    permintaan5 = Pengajuan.objects.filter(status=3)
    konteks = {
        'permintaan5' : permintaan5,
    }
    return render(request,'laporan_all.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Planning and Governance'])
def pengajuan_gh_pgo(request):
    permintaan6 = Pengajuan.objects.filter(group_id='Planning and Governance')
    permintaanex = Pengajuan.objects.filter(group_id='Sekum Divisi IT') 
    konteks = { 
        'permintaan6' : permintaan6,
        'permintaanex' : permintaanex,
    }
    return render(request,'pengajuan_pemimpin_pgo.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Planning and Governance'])
def hasiltindaklanjut_gh_pgo(request):
    permintaan7 = Pengajuan.objects.filter(htl=1)
    konteks = {
        'permintaan7' : permintaan7,
    }
    return render(request,'hasiltindaklanjut_pemimpin_pgo.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Planning and Governance'])
def approve_pgo(request, id_pengajuan_gh_pgo):
    pengajuan_gh_pgo = Pengajuan.objects.get(id=id_pengajuan_gh_pgo)
    pengajuan_gh_pgo.status=1
    pengajuan_gh_pgo.tl=1
    pengajuan_gh_pgo.save()
    messages.success(request, "Data Approved")

    return redirect('pengajuan_gh_pgo')

@login_required
@allowed_users(allowed_roles=['GH Planning and Governance'])
def disapprove_pgo(request, id_pengajuan_gh_pgo):
    pengajuan_gh_pgo = Pengajuan.objects.get(id=id_pengajuan_gh_pgo)
    pengajuan_gh_pgo.status=5
    pengajuan_gh_pgo.tl=0
    pengajuan_gh_pgo.save()
    messages.warning(request, "Data Rejected")

    return redirect('pengajuan_gh_pgo')

@login_required
@allowed_users(allowed_roles=['GH Planning and Governance'])
def approve_pgo2(request, id_hasiltindaklanjut_gh_pgo):
    hasiltindaklanjut_gh_pgo = Pengajuan.objects.get(id=id_hasiltindaklanjut_gh_pgo)
    a = hasiltindaklanjut_gh_pgo.jumlah
    hasiltindaklanjut_gh_pgo.status=3
    hasiltindaklanjut_gh_pgo.jumlah2=a
    hasiltindaklanjut_gh_pgo.save()
    messages.success(request, "Data Approved")

    return redirect('hasiltindaklanjut_gh_pgo')

@login_required
@allowed_users(allowed_roles=['GH Planning and Governance'])
def disapprove_pgo2(request, id_hasiltindaklanjut_gh_pgo):
    hasiltindaklanjut_gh_pgo = Pengajuan.objects.get(id=id_hasiltindaklanjut_gh_pgo)
    hasiltindaklanjut_gh_pgo.status=5
    hasiltindaklanjut_gh_pgo.save()
    messages.warning(request, "Data Rejected")

    return redirect('hasiltindaklanjut_gh_pgo')

# Pegawai Sekum Divisi IT (0)

@login_required
@allowed_users(allowed_roles=['Sekum Divisi IT'])
def home0(request):
    data4 = Pengajuan.objects.filter(group_id='Sekum Divisi IT').count()
    data5 = Pengajuan.objects.filter(group_id='Sekum Divisi IT', status='3').count()
    return render(request,'home0.html',{'data4' : data4, 'data5' : data5})

@login_required
@allowed_users(allowed_roles=['Sekum Divisi IT'])
def pengajuan0(request):
    permintaan8 = Pengajuan.objects.filter(group_id='Sekum Divisi IT')
    konteks = { 
        'permintaan8' : permintaan8,
    }
    return render(request,'pengajuan0.html',konteks)

def edithapus0(request, id_pengajuan0):
    pengajuan0 = Pengajuan.objects.get(id=id_pengajuan0)
    template = 'edithapus0.html'
    if request.POST:
        form = FormPengajuan(request.POST, instance=pengajuan0)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('pengajuan0')
    else:
        form = FormPengajuan(instance=pengajuan0)
        konteks = {
            'form':form,
            'pengajuan0':pengajuan0,
        }
    return render(request, template, konteks)

def delete0(request, id_pengajuan0):
    d0 = Pengajuan.objects.filter(id=id_pengajuan0)
    d0.delete()

    return redirect('pengajuan0')

@login_required
@allowed_users(allowed_roles=['Sekum Divisi IT'])
def tambah_pengajuan_0(request):
    if request.POST:
        form = FormPengajuan(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormPengajuan()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_pengajuan_0.html',konteks)

    else:
        form = FormPengajuan()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_pengajuan_0.html',konteks)

@login_required
@allowed_users(allowed_roles=['Sekum Divisi IT'])
def laporan0(request):
    permintaan9 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Sekum Divisi IT')
    konteks = {
        'permintaan9' : permintaan9,
    }
    return render(request,'laporan0.html',konteks)

# Pegawai Project Management (1)

@login_required
@allowed_users(allowed_roles=['Project Management'])
def home1(request):
    data8 = Pengajuan.objects.filter(group_id='Project Management').count()
    data9 = Pengajuan.objects.filter(group_id='Project Management', status='3').count()
    return render(request,'home1.html',{'data8' : data8, 'data9' : data9})

@login_required
@allowed_users(allowed_roles=['Project Management'])
def pengajuan1(request):
    permintaan12 = Pengajuan.objects.filter(group_id='Project Management')
    konteks = { 
        'permintaan12' : permintaan12,
    }
    return render(request,'pengajuan1.html',konteks)

def edithapus1(request, id_pengajuan1):
    pengajuan1 = Pengajuan.objects.get(id=id_pengajuan1)
    template = 'edithapus1.html'
    if request.POST:
        form = FormPengajuan(request.POST, instance=pengajuan1)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('pengajuan1')
    else:
        form = FormPengajuan(instance=pengajuan1)
        konteks = {
            'form':form,
            'pengajuan1':pengajuan1,
        }
    return render(request, template, konteks)

def delete1(request, id_pengajuan1):
    d1 = Pengajuan.objects.filter(id=id_pengajuan1)
    d1.delete()

    return redirect('pengajuan1')

@login_required
@allowed_users(allowed_roles=['Project Management'])
def tambah_pengajuan_1(request):
    if request.POST:
        form = FormPengajuan(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormPengajuan()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_pengajuan_1.html',konteks)

    else:
        form = FormPengajuan()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_pengajuan_1.html',konteks)

@login_required
@allowed_users(allowed_roles=['Project Management'])
def laporan1(request):
    permintaan13 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Project Management')
    konteks = {
        'permintaan13' : permintaan13,
    }
    return render(request,'laporan1.html',konteks)

# Group Head Project Management (1)

@login_required
@allowed_users(allowed_roles=['GH Project Management'])
def home_gh_1(request):
    data21 = Pengajuan.objects.filter(group_id='Project Management', status=0).count()
    return render(request,'home_gh_1.html',{'data21' : data21})

@login_required
@allowed_users(allowed_roles=['GH Project Management'])
def pengajuan_gh_1(request):
    permintaan14 = Pengajuan.objects.filter(group_id='Project Management')
    konteks = { 
        'permintaan14' : permintaan14,
    }
    return render(request,'pengajuan_gh_1.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Project Management'])
def laporan_gh_1(request):
    permintaan15 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Project Management')
    konteks = {
        'permintaan15' : permintaan15,
    }
    return render(request,'laporan_gh_1.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Project Management'])
def approve1(request, id_pengajuan_gh_1):
    pengajuan_gh_1 = Pengajuan.objects.get(id=id_pengajuan_gh_1)
    pengajuan_gh_1.tl=1
    pengajuan_gh_1.status=1
    pengajuan_gh_1.save()
    messages.success(request, "Data Approved")

    return redirect('pengajuan_gh_1')

@login_required
@allowed_users(allowed_roles=['GH Project Management'])
def disapprove1(request, id_pengajuan_gh_1):
    pengajuan_gh_1 = Pengajuan.objects.get(id=id_pengajuan_gh_1)
    pengajuan_gh_1.tl=0
    pengajuan_gh_1.status=5
    pengajuan_gh_1.save()
    messages.warning(request, "Data Rejected")

    return redirect('pengajuan_gh_1')

# Pegawai Business Intelligence & Analythic (2)

@login_required
@allowed_users(allowed_roles=['Business Intelligence & Analythic'])
def home2(request):
    data10 = Pengajuan.objects.filter(group_id='Business Intelligence & Analythic').count()
    data11 = Pengajuan.objects.filter(group_id='Business Intelligence & Analythic', status='3').count()
    return render(request,'home2.html',{'data10' : data10, 'data11' : data11})

@login_required
@allowed_users(allowed_roles=['Business Intelligence & Analythic'])
def pengajuan2(request):
    permintaan16 = Pengajuan.objects.filter(group_id='Business Intelligence & Analythic')
    konteks = { 
        'permintaan16' : permintaan16,
    }
    return render(request,'pengajuan2.html',konteks)

def edithapus2(request, id_pengajuan2):
    pengajuan2 = Pengajuan.objects.get(id=id_pengajuan2)
    template = 'edithapus2.html'
    if request.POST:
        form = FormPengajuan(request.POST, instance=pengajuan2)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('pengajuan2')
    else:
        form = FormPengajuan(instance=pengajuan2)
        konteks = {
            'form':form,
            'pengajuan2':pengajuan2,
        }
    return render(request, template, konteks)

def delete2(request, id_pengajuan2):
    d2 = Pengajuan.objects.filter(id=id_pengajuan2)
    d2.delete()

    return redirect('pengajuan2')

@login_required
@allowed_users(allowed_roles=['Business Intelligence & Analythic'])
def tambah_pengajuan_2(request):
    if request.POST:
        form = FormPengajuan(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormPengajuan()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_pengajuan_2.html',konteks)

    else:
        form = FormPengajuan()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_pengajuan_2.html',konteks)

@login_required
@allowed_users(allowed_roles=['Business Intelligence & Analythic'])
def laporan2(request):
    permintaan17 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Business Intelligence & Analythic')
    konteks = {
        'permintaan17' : permintaan17,
    }
    return render(request,'laporan2.html',konteks)

# Group Head Business Intelligence & Analythic (2)

@login_required
@allowed_users(allowed_roles=['GH Business Intelligence & Analythic'])
def home_gh_2(request):
    data22 = Pengajuan.objects.filter(group_id='Business Intelligence & Analythic', status=0).count()
    return render(request,'home_gh_2.html',{'data22' : data22})

@login_required
@allowed_users(allowed_roles=['GH Business Intelligence & Analythic'])
def pengajuan_gh_2(request):
    permintaan18 = Pengajuan.objects.filter(group_id='Business Intelligence & Analythic')
    konteks = { 
        'permintaan18' : permintaan18,
    }
    return render(request,'pengajuan_gh_2.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Business Intelligence & Analythic'])
def laporan_gh_2(request):
    permintaan19 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Business Intelligence & Analythic')
    konteks = {
        'permintaan19' : permintaan19,
    }
    return render(request,'laporan_gh_2.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Business Intelligence & Analythic'])
def approve2(request, id_pengajuan_gh_2):
    pengajuan_gh_2 = Pengajuan.objects.get(id=id_pengajuan_gh_2)
    pengajuan_gh_2.tl=1
    pengajuan_gh_2.status=1
    pengajuan_gh_2.save()
    messages.success(request, "Data Approved")

    return redirect('pengajuan_gh_2')

@login_required
@allowed_users(allowed_roles=['GH Business Intelligence & Analythic'])
def disapprove2(request, id_pengajuan_gh_2):
    pengajuan_gh_2 = Pengajuan.objects.get(id=id_pengajuan_gh_2)
    pengajuan_gh_2.tl=0
    pengajuan_gh_2.status=5
    pengajuan_gh_2.save()
    messages.warning(request, "Data Rejected")

    return redirect('pengajuan_gh_2')


# Pegawai Application Management Core & Non Core (3)

@login_required
@allowed_users(allowed_roles=['Application Management Core & Non Core'])
def home3(request):
    data12 = Pengajuan.objects.filter(group_id='Application Management Core & Non Core').count()
    data13 = Pengajuan.objects.filter(group_id='Application Management Core & Non Core', status='3').count()
    return render(request,'home3.html',{'data12' : data12, 'data13' : data13})

@login_required
@allowed_users(allowed_roles=['Application Management Core & Non Core'])
def pengajuan3(request):
    permintaan20 = Pengajuan.objects.filter(group_id='Application Management Core & Non Core')
    konteks = { 
        'permintaan20' : permintaan20,
    }
    return render(request,'pengajuan3.html',konteks)

def edithapus3(request, id_pengajuan3):
    pengajuan3 = Pengajuan.objects.get(id=id_pengajuan3)
    template = 'edithapus3.html'
    if request.POST:
        form = FormPengajuan(request.POST, instance=pengajuan3)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('pengajuan3')
    else:
        form = FormPengajuan(instance=pengajuan3)
        konteks = {
            'form':form,
            'pengajuan3':pengajuan3,
        }
    return render(request, template, konteks)

def delete3(request, id_pengajuan3):
    d3 = Pengajuan.objects.filter(id=id_pengajuan3)
    d3.delete()

    return redirect('pengajuan3')

@login_required
@allowed_users(allowed_roles=['Application Management Core & Non Core'])
def tambah_pengajuan_3(request):
    if request.POST:
        form = FormPengajuan(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormPengajuan()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_pengajuan_3.html',konteks)

    else:
        form = FormPengajuan()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_pengajuan_3.html',konteks)

@login_required
@allowed_users(allowed_roles=['Application Management Core & Non Core'])
def laporan3(request):
    permintaan21 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Application Management Core & Non Core')
    konteks = {
        'permintaan21' : permintaan21,
    }
    return render(request,'laporan3.html',konteks)

# Group Head Application Management Core & Non Core (3)

@login_required
@allowed_users(allowed_roles=['GH Application Management Core & Non Core'])
def home_gh_3(request):
    data23 = Pengajuan.objects.filter(group_id='Application Management Core & Non Core', status=0).count()
    return render(request,'home_gh_3.html',{'data23' : data23})

@login_required
@allowed_users(allowed_roles=['GH Application Management Core & Non Core'])
def pengajuan_gh_3(request):
    permintaan22 = Pengajuan.objects.filter(group_id='Application Management Core & Non Core')
    konteks = { 
        'permintaan22' : permintaan22,
    }
    return render(request,'pengajuan_gh_3.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Application Management Core & Non Core'])
def laporan_gh_3(request):
    permintaan23 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Application Management Core & Non Core')
    konteks = {
        'permintaan23' : permintaan23,
    }
    return render(request,'laporan_gh_3.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Application Management Core & Non Core'])
def approve3(request, id_pengajuan_gh_3):
    pengajuan_gh_3 = Pengajuan.objects.get(id=id_pengajuan_gh_3)
    pengajuan_gh_3.tl=1
    pengajuan_gh_3.status=1
    pengajuan_gh_3.save()
    messages.success(request, "Data Approved")

    return redirect('pengajuan_gh_3')

@login_required
@allowed_users(allowed_roles=['GH Application Management Core & Non Core'])
def disapprove3(request, id_pengajuan_gh_3):
    pengajuan_gh_3 = Pengajuan.objects.get(id=id_pengajuan_gh_3)
    pengajuan_gh_3.tl=0
    pengajuan_gh_3.status=5
    pengajuan_gh_3.save()
    messages.warning(request, "Data Rejected")

    return redirect('pengajuan_gh_3')


# Pegawai Network, Security & Risk Management (4)

@login_required
@allowed_users(allowed_roles=['Network, Security & Risk Management'])
def home4(request):
    data14 = Pengajuan.objects.filter(group_id='Network, Security & Risk Management').count()
    data15 = Pengajuan.objects.filter(group_id='Network, Security & Risk Management', status='3').count()
    return render(request,'home4.html',{'data14' : data14, 'data15' : data15})

@login_required
@allowed_users(allowed_roles=['Network, Security & Risk Management'])
def pengajuan4(request):
    permintaan24 = Pengajuan.objects.filter(group_id='Network, Security & Risk Management')
    konteks = { 
        'permintaan24' : permintaan24,
    }
    return render(request,'pengajuan4.html',konteks)

def edithapus4(request, id_pengajuan4):
    pengajuan4 = Pengajuan.objects.get(id=id_pengajuan4)
    template = 'edithapus4.html'
    if request.POST:
        form = FormPengajuan(request.POST, instance=pengajuan4)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('pengajuan4')
    else:
        form = FormPengajuan(instance=pengajuan4)
        konteks = {
            'form':form,
            'pengajuan4':pengajuan4,
        }
    return render(request, template, konteks)

def delete4(request, id_pengajuan4):
    d4 = Pengajuan.objects.filter(id=id_pengajuan4)
    d4.delete()

    return redirect('pengajuan4')

@login_required
@allowed_users(allowed_roles=['Network, Security & Risk Management'])
def tambah_pengajuan_4(request):
    if request.POST:
        form = FormPengajuan(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormPengajuan()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_pengajuan_4.html',konteks)

    else:
        form = FormPengajuan()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_pengajuan_4.html',konteks)

@login_required
@allowed_users(allowed_roles=['Network, Security & Risk Management'])
def laporan4(request):
    permintaan25 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Network, Security & Risk Management')
    konteks = {
        'permintaan25' : permintaan25,
    }
    return render(request,'laporan4.html',konteks)

# Group Head Network, Security & Risk Management (4)

#@login_required
#@allowed_users(allowed_roles=['GH Network, Security & Risk Management'])
def home_gh_4(request):
    data24 = Pengajuan.objects.filter(group_id='Network, Security & Risk Management', status=0).count()
    return render(request,'home_gh_4.html',{'data24' : data24})

#login_required
#allowed_users(allowed_roles=['GH Network, Security & Risk Management'])
def pengajuan_gh_4(request):
    permintaan26 = Pengajuan.objects.filter(group_id='Network, Security & Risk Management')
    konteks = { 
        'permintaan26' : permintaan26,
    }
    return render(request,'pengajuan_gh_4.html',konteks)

#@login_required
#@allowed_users(allowed_roles=['GH Network, Security & Risk Management'])
def laporan_gh_4(request):
    permintaan27 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Network, Security & Risk Management')
    konteks = {
        'permintaan27' : permintaan27,
    }
    return render(request,'laporan_gh_4.html',konteks)

#login_required
#allowed_users(allowed_roles=['GH Network, Security & Risk Management'])
def approve4(request, id_pengajuan_gh_4):
    pengajuan_gh_4 = Pengajuan.objects.get(id=id_pengajuan_gh_4)
    pengajuan_gh_4.tl=1
    pengajuan_gh_4.status=1
    pengajuan_gh_4.save()
    messages.success(request, "Data Approved")

    return redirect('pengajuan_gh_4')

#login_required
#allowed_users(allowed_roles=['GH Network, Security & Risk Management'])
def disapprove4(request, id_pengajuan_gh_4):
    pengajuan_gh_4 = Pengajuan.objects.get(id=id_pengajuan_gh_4)
    pengajuan_gh_4.tl=1
    pengajuan_gh_4.status=5
    pengajuan_gh_4.save()
    messages.warning(request, "Data Rejected")

    return redirect('pengajuan_gh_4')


# Pegawai Operation Management DC & DRC (5)

@login_required
@allowed_users(allowed_roles=['Operation Management DC & DRC'])
def home5(request):
    data16 = Pengajuan.objects.filter(group_id='Operation Management DC & DRC').count()
    data17 = Pengajuan.objects.filter(group_id='Operation Management DC & DRC', status='3').count()
    return render(request,'home5.html',{'data16' : data16, 'data17' : data17})

@login_required
@allowed_users(allowed_roles=['Operation Management DC & DRC'])
def pengajuan5(request):
    permintaan28 = Pengajuan.objects.filter(group_id='Operation Management DC & DRC')
    konteks = { 
        'permintaan28' : permintaan28,
    }
    return render(request,'pengajuan5.html',konteks)

def edithapus5(request, id_pengajuan5):
    pengajuan5 = Pengajuan.objects.get(id=id_pengajuan5)
    template = 'edithapus5.html'
    if request.POST:
        form = FormPengajuan(request.POST, instance=pengajuan5)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('pengajuan5')
    else:
        form = FormPengajuan(instance=pengajuan5)
        konteks = {
            'form':form,
            'pengajuan5':pengajuan5,
        }
    return render(request, template, konteks)

def delete5(request, id_pengajuan5):
    d5 = Pengajuan.objects.filter(id=id_pengajuan5)
    d5.delete()

    return redirect('pengajuan5')

@login_required
@allowed_users(allowed_roles=['Operation Management DC & DRC'])
def tambah_pengajuan_5(request):
    if request.POST:
        form = FormPengajuan(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormPengajuan()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_pengajuan_5.html',konteks)

    else:
        form = FormPengajuan()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_pengajuan_5.html',konteks)

@login_required
@allowed_users(allowed_roles=['Operation Management DC & DRC'])
def laporan5(request):
    permintaan29 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Operation Management DC & DRC')
    konteks = {
        'permintaan29' : permintaan29,
    }
    return render(request,'laporan5.html',konteks)

# Group Head Operation Management DC & DRC (5)

@login_required
@allowed_users(allowed_roles=['GH Operation Management DC & DRC'])
def home_gh_5(request):
    data25 = Pengajuan.objects.filter(group_id='Operation Management DC & DRC', status=0).count()
    return render(request,'home_gh_5.html',{'data25' : data25})

@login_required
@allowed_users(allowed_roles=['Operation Management DC & DRC'])
def pengajuan_gh_5(request):
    permintaan30 = Pengajuan.objects.filter(group_id='Operation Management DC & DRC')
    konteks = { 
        'permintaan30' : permintaan30,
    }
    return render(request,'pengajuan_gh_5.html',konteks)

@login_required
@allowed_users(allowed_roles=['Operation Management DC & DRC'])
def laporan_gh_5(request):
    permintaan31 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Operation Management DC & DRC')
    konteks = {
        'permintaan31' : permintaan31,
    }
    return render(request,'laporan_gh_5.html',konteks)

@login_required
@allowed_users(allowed_roles=['Operation Management DC & DRC'])
def approve5(request, id_pengajuan_gh_5):
    pengajuan_gh_5 = Pengajuan.objects.get(id=id_pengajuan_gh_5)
    pengajuan_gh_5.tl=1
    pengajuan_gh_5.status=1
    pengajuan_gh_5.save()
    messages.success(request, "Data Approved")

    return redirect('pengajuan_gh_5')

@login_required
@allowed_users(allowed_roles=['Operation Management DC & DRC'])
def disapprove5(request, id_pengajuan_gh_5):
    pengajuan_gh_5 = Pengajuan.objects.get(id=id_pengajuan_gh_5)
    pengajuan_gh_5.tl=0
    pengajuan_gh_5.status=5
    pengajuan_gh_5.save()
    messages.warning(request, "Data Rejected")

    return redirect('pengajuan_gh_5')

# Pegawai Helpdesk & Support (6)

@login_required
@allowed_users(allowed_roles=['Helpdesk & Support'])
def home6(request):
    data18 = Pengajuan.objects.filter(group_id='Helpdesk & Support').count()
    data19 = Pengajuan.objects.filter(group_id='Helpdesk & Support', status='3').count()
    return render(request,'home6.html',{'data18' : data18, 'data19' : data19})

@login_required
@allowed_users(allowed_roles=['Helpdesk & Support'])
def pengajuan6(request):
    permintaan32 = Pengajuan.objects.filter(group_id='Helpdesk & Support')
    konteks = { 
        'permintaan32' : permintaan32,
    }
    return render(request,'pengajuan6.html',konteks)

def edithapus6(request, id_pengajuan6):
    pengajuan6 = Pengajuan.objects.get(id=id_pengajuan6)
    template = 'edithapus6.html'
    if request.POST:
        form = FormPengajuan(request.POST, instance=pengajuan6)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Disimpan")
            return redirect('pengajuan6')
    else:
        form = FormPengajuan(instance=pengajuan6)
        konteks = {
            'form':form,
            'pengajuan6':pengajuan6,
        }
    return render(request, template, konteks)

def delete6(request, id_pengajuan6):
    d6 = Pengajuan.objects.filter(id=id_pengajuan6)
    d6.delete()

    return redirect('pengajuan6')

@login_required
@allowed_users(allowed_roles=['Helpdesk & Support'])
def tambah_pengajuan_6(request):
    if request.POST:
        form = FormPengajuan(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormPengajuan()
            pesan = "data berhasil di simpan"
            konteks = {
            'form' : form,
            'pesan' : pesan
            }
            return render(request, 'tambah_pengajuan_6.html',konteks)

    else:
        form = FormPengajuan()

        konteks = {
        'form' : form,
        }

        return render(request, 'tambah_pengajuan_6.html',konteks)

@login_required
@allowed_users(allowed_roles=['Helpdesk & Support'])
def laporan6(request):
    permintaan33 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Helpdesk & Support')
    konteks = {
        'permintaan33' : permintaan33,
    }
    return render(request,'laporan6.html',konteks)

# Group Head Helpdesk & Support (6)

@login_required
@allowed_users(allowed_roles=['GH Helpdesk & Support'])
def home_gh_6(request):
    data26 = Pengajuan.objects.filter(group_id='Helpdesk & Support', status=0).count()
    return render(request,'home_gh_6.html',{'data26' : data26})

@login_required
@allowed_users(allowed_roles=['GH Helpdesk & Support'])
def pengajuan_gh_6(request):
    permintaan34 = Pengajuan.objects.filter(group_id='Helpdesk & Support')
    konteks = { 
        'permintaan34' : permintaan34,
    }
    return render(request,'pengajuan_gh_6.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Helpdesk & Support'])
def laporan_gh_6(request):
    permintaan35 = Pengajuan.objects.filter(status=3) & Pengajuan.objects.filter(group_id='Helpdesk & Support')
    konteks = {
        'permintaan35' : permintaan35,
    }
    return render(request,'laporan_gh_6.html',konteks)

@login_required
@allowed_users(allowed_roles=['GH Helpdesk & Support'])
def approve6(request, id_pengajuan_gh_6):
    pengajuan_gh_6 = Pengajuan.objects.get(id=id_pengajuan_gh_6)
    pengajuan_gh_6.tl=1
    pengajuan_gh_6.status=1
    pengajuan_gh_6.save()
    messages.success(request, "Data Approved")

    return redirect('pengajuan_gh_6')

@login_required
@allowed_users(allowed_roles=['GH Helpdesk & Support'])
def disapprove6(request, id_pengajuan_gh_6):
    pengajuan_gh_6 = Pengajuan.objects.get(id=id_pengajuan_gh_6)
    pengajuan_gh_6.tl=1
    pengajuan_gh_6.status=5
    pengajuan_gh_6.save()
    messages.warning(request, "Data Rejected")


    return redirect('pengajuan_gh_6')


#Mencetak Excel

@login_required
def export_xls(request):
    pengajuan = PengajuanResource()
    dataset = pengajuan.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment: filename="Laporan Pengajuan.xls"'
    return response

@login_required
def export_xls2(request):
    terima = TerimaResource()
    dataset = terima.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment: filename="Laporan Serah Terima.xls"'
    return response

#Mencetak PDF

# def link_callback(uri, rel):
#             """
#             Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#             resources
#             """
#             result = finders.find(uri)
#             if result:
#                     if not isinstance(result, (list, tuple)):
#                             result = [result]
#                     result = list(os.path.realpath(path) for path in result)
#                     path=result[0]
#             else:
#                     sUrl = settings.STATIC_URL        # Typically /static/
#                     sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
#                     mUrl = settings.MEDIA_URL         # Typically /media/
#                     mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

#                     if uri.startswith(mUrl):
#                             path = os.path.join(mRoot, uri.replace(mUrl, ""))
#                     elif uri.startswith(sUrl):
#                             path = os.path.join(sRoot, uri.replace(sUrl, ""))
#                     else:
#                             return uri

#             # make sure that file exists
#             if not os.path.isfile(path):
#                     raise Exception(
#                             'media URI must start with %s or %s' % (sUrl, mUrl)
#                     )
#             return path

def terima_render_pdf(request,*args,**kwargs):
    pk = kwargs.get('pk')
    terima = get_object_or_404(Terima, pk=pk)
    template_path = 'pdf_page.html'
    context = {'terima':terima}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="BJB.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    links = lambda uri,rel:os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=links)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def stock_detail(request, pk):
    queryset = Pengajuan.objects.get(id=pk) 
    context = {
        'queryset': queryset,
    }
    return render(request, "stock_detail.html", context)

def issue_items(request, pk):
    queryset = Pengajuan.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.jumlah2 -= instance.issue_quantity  
        instance.issue_by = str(request.user)
        instance.save()
        return redirect('/stock_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)


def receive_items(request, pk):
    queryset = Pengajuan.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.jumlah2 += instance.receive_quantity 
        instance.receive_by = str(request.user)
        instance.save()
        return redirect('/stock_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
            
            "instance": queryset,
            "form": form,
            "username": 'Receive By: ' + str(request.user),
        }
    return render(request, "add_items.html", context)


    