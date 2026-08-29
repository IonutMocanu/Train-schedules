from django.contrib import admin
from .models import Train, Station, Cursa, Stop

# Register your models here.
class TrainAdmin(admin.ModelAdmin):
    list_display = ('train_number', 'company', 'train_type')
    search_fields = ('train_number', 'company', 'train_type')
    list_filter = ('company', 'train_type')

admin.site.register(Train, TrainAdmin)

class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'longitude', 'latitude')
    search_fields = ('name', 'city')
    list_filter = ('city',)

admin.site.register(Station, StationAdmin)

class CursaAdmin(admin.ModelAdmin):
    list_display = ('get_train_number', 'date', 'status')
    search_fields = ('train', 'date', 'status')
    list_filter = ('status', 'date')

    # Definim metoda care extrage numărul trenului pentru a-l afișa în tabel
    def get_train_number(self, obj):
        return obj.train.train_number
    
    # Opțional: cum să se numească coloana în tabelul din panoul de admin
    get_train_number.short_description = 'Număr Tren'
    
    # Opțional: permite sortarea (când dai click pe antetul coloanei)
    get_train_number.admin_order_field = 'train__train_number'

admin.site.register(Cursa, CursaAdmin)

class StopAdmin(admin.ModelAdmin):
    list_display = ('get_cursa_train_number', 'get_data', 'station', 'arrival_time', 'departure_time', 'sequence_number', 'delay_minutes')
    search_fields = ('cursa__train__train_number', 'station')
    list_filter = ('cursa', 'station__city')

    def get_cursa_train_number(self, obj):
        return obj.cursa.train.train_number

    get_cursa_train_number.short_description = 'Cursa - Număr Tren'
    
    # Opțional: permite sortarea (când dai click pe antetul coloanei)
    get_cursa_train_number.admin_order_field = 'cursa__train__train_number'

    def get_data(self, obj):
        return obj.cursa.date

    get_data.short_description = 'Data Cursă'
    get_data.admin_order_field = 'cursa__date'

admin.site.register(Stop, StopAdmin)