from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Journal, ScientificEditors, Category, Genre, Issues, Items


@admin.register(Issues)  # декоратор
class IssuesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "journal", "publication_date")
    list_filter = ("publication_date",)
    actions = ["publish", "unpublish"]
    search_fields = ("name",)
    list_display_links = ("name",)
    # list_editable = ("draft",)
    save_on_top = True
    save_as = True

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = "{row_update} записей были обновлены"
        self.message_user(request, "{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = "{row_update} записей были обновлены"
        self.message_user(request, "{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)


@admin.register(Journal)  # декоратор
class JournalAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_image", "publication_date", "draft")
    readonly_fields = ("get_image",)  # запрет на редактирование
    list_display_links = ("name",)
    list_filter = ("publication_date",)
    actions = ["publish", "unpublish"]
    search_fields = ("name", "category__name",)
    list_editable = ("draft",)
    save_on_top = True
    save_as = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="60" height="60"')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = "{row_update} записей были обновлены"
        self.message_user(request, "{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = "{row_update} записей были обновлены"
        self.message_user(request, "{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Изображение"

    # fieldsets = (
    #     ("Основная информация", {
    #         "fields": (("name", "publication_date", "country"),)
    #     }),
    #     (None, {
    #         "fields": (("category", "genres"),)
    #     }),
    #     (None, {
    #         "fields": ("description",)
    #     }),
    #     ("Изображения", {
    #         "fields": (("get_image", "image"),)
    #     }),
    #     (None, {
    #         "fields": ("editors",)
    #     }),
    #     ("Настройки", {
    #         "fields": ("draft",)
    #     }),
    # )
#
#


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ScientificEditors)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Items)


admin.site.site_title = "Django Library"
admin.site.site_header = "Django Library"
