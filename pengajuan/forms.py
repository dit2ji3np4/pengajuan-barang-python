from django.contrib.auth.models import User, Group
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from pengajuan.models import *
from django import forms

class FormPengajuan(ModelForm):
    class Meta:
        model = Pengajuan
        exclude = ['nomor_memo', 'jumlah2', 'tanggal_memo', 'perihal_memo', 'harga_barang', 'nomor_barang', 'nama_pemilik', 'status', 'tl', 'htl']
 
        widgets = {
            'nik' : forms.TextInput({'class':'form-control'}),
            'group_id' : forms.TextInput({'class':'form-control', 'readonly':'readonly'}),
            'id_pengajuan' : forms.TextInput({'class':'form-control'}), 
            'nama_barang' : forms.TextInput({'class':'form-control'}), 
            'spesifikasi' : forms.TextInput({'class':'form-control'}), 
            'jumlah' : forms.NumberInput({'class':'form-control'}), 
            'landasan_kebutuhan' : forms.TextInput({'class':'form-control'}), 
        }

class FormTindaklanjut(ModelForm):
    class Meta:
        model = Pengajuan
        exclude = ['nomor_barang', 'nama_pemilik', 'tl', 'jumlah2']

        widgets = {
            'group_id' : forms.TextInput({'class':'form-control', 'readonly':'readonly'}),
            'status' : forms.NumberInput({'class':'form-control'}),
            'htl' : forms.NumberInput({'class':'form-control'}),
            'tanggal_memo' : forms.TextInput({'class':'form-control','type':'date'}),
        }



class FormTambahketerangan(ModelForm):
    class Meta:
        model = Pengajuan
        fields = '__all__'

        widgets = {
            'status' : forms.NumberInput({'class':'form-control'}),
        }

class FormTerima(ModelForm):
    class Meta:
        model = Terima
        exclude = ['nomor_barang']

        widgets = {
            'nama_pemilik' : forms.TextInput({'class':'form-control'}),
            'pengajuans' : forms.Select({'class':'form-control'}),
            'divisi' : forms.TextInput({'class':'form-control', 'readonly':'readonly'}),
            'merk' : forms.TextInput({'class':'form-control'}), 
            'jabatan' : forms.TextInput({'class':'form-control'}), 
            'tanggal_terima' : forms.TextInput({'class':'form-control','type':'date'}), 
            'tipe' : forms.TextInput({'class':'form-control'}),
            'nama_penyerah' : forms.TextInput({'class':'form-control'}),
            'pemimpin_user' : forms.TextInput({'class':'form-control'}),
            'pemimpin_pgo' : forms.TextInput({'class':'form-control', 'readonly':'readonly'}),
        }

class UserProfileForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2', 'group']

        widgets = {
            
        }