from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from library import views

urlpatterns = [
    path('', views.JournalView.as_view(), name="home"),
    path("filter/", views.FilterJournalView.as_view(), name="filter"),
    path("create_user/", views.register, name="create_user"),
    path("search/", views.Search.as_view(), name="search"),
    path("create_journal/", views.create_journal, name="create_journal"),
    path("create_issues/", views.create_issues, name="create_issues"),
    path("create_items/", views.create_items, name="create_items"),
    path("<str:slug>/update_issues", views.IssuesUpdateView.as_view(), name="issues_update"),
    path("<str:slug>/update_journal", views.JournalUpdateView.as_view(), name="journal_update"),
    path("<str:slug>/update_items", views.ItemsUpdateView.as_view(), name="items_update"),
    path("<int:pk>/delete_journal", views.JournalDeleteView.as_view(), name="journal_delete"),
    path("<int:pk>/delete_issues", views.IssuesDeleteView.as_view(), name="issues_delete"),
    path("<int:pk>/delete_items", views.ItemsDeleteView.as_view(), name="items_delete"),
    path("<str:slug>/", views.JournalDetailView.as_view(), name="journal_detail"),
    path("journal/<str:slug>/", views.IssuesDetailView.as_view(), name="issues_detail"),
    path("issues/<str:slug>/", views.ItemsDetailView.as_view(), name="items_detail"),
    path("editor/<str:slug>/", views.EditorView.as_view(), name="editor_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
