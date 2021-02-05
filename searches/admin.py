from django.contrib import admin


from searches.models import SearchArea, TelegramUser, SearchRequest


@admin.register(SearchArea, TelegramUser, SearchRequest)
class SearchesAdmin(admin.ModelAdmin):
    pass