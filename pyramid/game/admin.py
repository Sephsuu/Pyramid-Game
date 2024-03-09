from django.contrib import admin
from .models import *
# Register your models here.

class StudentsAdmin(admin.ModelAdmin):
    list_display = ('stud_id', 'last_name', 'first_name', 'user')
    ordering = ('last_name',)
    

class VoteAdmin(admin.ModelAdmin):
    list_display = ('get_voter_last_name', 'get_recipient_last_name', 'vote_count')

    def get_voter_last_name(self, obj):
        return obj.voter.last_name
    
    def get_recipient_last_name(self, obj):
        return obj.recipient.last_name
    
    get_voter_last_name.short_description = 'Voter Last Name'
    get_recipient_last_name.short_description = 'Recipient Last Name'

admin.site.register(Students, StudentsAdmin)
admin.site.register(Vote, VoteAdmin)