
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from image.views import UserCreateView, IndexView, ImageDetailView, CommentCreateView ,\
                        ImageCreateView, ImageUpdateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^create_user/$', UserCreateView.as_view(), name="user_create_view"),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^image/(?P<pk>\d+)/$', ImageDetailView.as_view(), name='image_detail_view'),
    url(r'^image/(?P<pk>\d+)/comment/$', CommentCreateView.as_view(), name='comment_create_view'),
    url(r'^image/create/$', ImageCreateView.as_view(), name='image_create_view'),
    url(r'^image/(?P<pk>\d+)/update/$', ImageUpdateView.as_view(), name='image_update_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
