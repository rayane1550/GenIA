from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Esta linha substitui o seu antigo 'login/', 'api/token/', etc.
    # Ela cria automaticamente as rotas de login e logout para o React
    path('api/auth/', include('dj_rest_auth.urls')),
    
    # Rota para o fluxo do Google e Allauth
    path('accounts/', include('allauth.urls')),
    
    # Suas rotas da API (certifique-se que a pasta se chama 'Api' com A maiúsculo)
    path('Api/', include('Api.urls')),
]