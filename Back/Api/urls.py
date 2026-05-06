from .views import RegisterViewSet
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




from .views import *

router = DefaultRouter()

router.register(r'usuario', UsuarioViewSet)
router.register(r'mensagem', MensagemViewSet)
router.register(r'conversa', ConversaViewSet)
router.register(r'modeloAI', ModeloIAViewSet)


urlpatterns = [
    path ('tokien', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('register/', RegisterViewSet.as_view()),
    path('', include(router.urls)),
    


    path('importar_usuario/', importar_usuario),
    path('importar_conversa/', importar_conversa),
    path('importar_mensagem/', importar_mensagem),
    path('importar_modeloAI/', importar_modeloAI),

    path('', include(router.urls)),
]