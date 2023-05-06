from django.contrib import admin
from .models import Beat, Types, Tonal


class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('duration', 'bpm')


class SaveData(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.get_bpm_and_duration()
        super().save_model(request, obj, form, change)


class BeatAdmin(PersonAdmin, SaveData):
    pass


admin.site.register(Beat, BeatAdmin)
admin.site.register(Types)
admin.site.register(Tonal)
