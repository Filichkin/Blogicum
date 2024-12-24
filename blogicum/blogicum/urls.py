from django.contrib import admin
from django.urls import include, path


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'


urlpatterns = [
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
]
