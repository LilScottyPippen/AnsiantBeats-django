from django.contrib import admin
from .models import Beat, Types, Tonal


class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('duration',)


admin.site.register(Beat, PersonAdmin)
admin.site.register(Types)
admin.site.register(Tonal)
