"""simplemooc URL Configuration
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#caso usar imagem, importar
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cursos/', include('courses.urls')),
    path('forum/', include('forum.urls')),
    #Registro usuario
    path('accounts/', include('accounts.urls')),
    #Login
    path('accounts/', include('django.contrib.auth.urls')),
]

# Para carregar as nossas imagens(se estiver no ambiente de desenvolvimento)
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
