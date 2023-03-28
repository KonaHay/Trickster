from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TricksterMain.urls')),
    path('Users/', include('django.contrib.auth.urls')),
    path('Users/', include('Users.urls')),
    path('quiz/', include('TricksterQuiz.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configure Admin Titles
admin.site.site_header = "Trickster Administration"
admin.site.site_title = "Trickster Admin"
admin.site.index_title = "Welcome to the Trickster Admin Panel"