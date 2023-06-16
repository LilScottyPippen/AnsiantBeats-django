from django.contrib import admin
from .models import Beat, Types, Tonal, Mood, License, Ticket, Coupone


class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('duration', 'bpm')


class SaveData(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.convert_drive_link()
        obj.get_bpm_and_duration()
        super().save_model(request, obj, form, change)


class BeatAdmin(PersonAdmin, SaveData):
    pass


admin.site.register(Beat, BeatAdmin)
admin.site.register(Types)
admin.site.register(Tonal)
admin.site.register(Mood)
admin.site.register(License)
admin.site.register(Ticket)
admin.site.register(Coupone)
