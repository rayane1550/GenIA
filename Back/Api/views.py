from django.shortcuts import render, redirect
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.decorators import api_view, action, permission_classes
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
from django.http import JsonResponse
from .models import Usuario

def login_view(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        try:
            usuario = Usuario.objects.get(email=email, senha=senha)

            request.session['usuario_id'] = usuario.id
            request.session['usuario_nome'] = usuario.nome
            request.session['usuario_tipo'] = usuario.tipo

            if usuario.tipo == 'admin':
                return redirect('/admin/')
            else:
                return redirect('/chat/')

        except Usuario.DoesNotExist:
            return redirect('/login/')



        






































def importar_usuario(request):
    return JsonResponse({"msg": "importar usuario ok"})

def importar_conversa(request):
    return JsonResponse({"msg": "importar conversa ok"})

def importar_mensagem(request):
    return JsonResponse({"msg": "importar mensagem ok"})

def importar_modeloAI(request):
    return JsonResponse({"msg": "importar modeloAI ok"})



class UsuarioViewSet(ModelViewSet): # viewset serve para criar as rotas automaticamente, não precisa criar uma view para cada ação
    queryset = Usuario.objects.all()# define a queryset para o viewset, ou seja, os dados que serão retornados quando uma requisição for feita para a rota do usuário. O queryset é uma forma de filtrar os dados que serão retornados, por exemplo, para retornar apenas os usuários ativos ou para retornar apenas os usuários com um determinado tipo.
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
 
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsuarioFilter
 
    def get_queryset(self): # def get_queryset(self) é um método que pode ser sobrescrito para personalizar a queryset retornada pelo viewset. No caso do usuário, queremos retornar apenas os dados do usuário logado, a menos que o usuário seja um superusuário (staff), nesse caso, ele pode ver todos os usuários.
        qs = super().get_queryset() # chama o método get_queryset() da classe pai (ModelViewSet) para obter a queryset padrão, que é definida como Usuario.objects.all(). Em seguida, verificamos se o usuário logado é um superusuário (staff). Se for, retornamos a queryset completa, permitindo que ele veja todos os usuários. Caso contrário, filtramos a queryset para retornar apenas o usuário logado, usando qs.filter(user=self.request.user). Isso garante que um usuário comum só possa acessar seus próprios dados, enquanto um superusuário pode acessar os dados de todos os usuários.
 
        if self.request.user.is_staff:
            return qs
       
        return qs.filter(user=self.request.user)
   
    def get_serializer_class(self):
        if self.action == "me":
            return UsuarioSerializer
        return super().get_serializer_class()
   
    @action(
        detail=False,
        methods=['get'],
        url_path="me",
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        usuario = Usuario.objects.filter(user=request.user).first()
        if not usuario:
            return Response({"detail":"Perfil de usuário não encontrado."}, status=404)
       
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)
   
    @action(
        detail=False,
        methods=['get'],
        url_path="tipo-choices",
        permission_classes=[AllowAny]
    )
    def tipo_choices(self, request):
        return Response([
            {"value": v, "label": l}
            for v, l in Usuario.TIPO_CHOICES
        ])
   
 
class RegisterViewSet(APIView):
    permission_classes=[AllowAny]
 
    def post(self, request):
        serializer = RegisterSerializer (data=request.data)
        if serializer.is_valid():
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"detail": "Usuário criado com sucesso."}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Erro ao criar o usuário."}, status=status.HTTP_400_BAD_REQUEST)



class MensagemViewSet(ModelViewSet):
    queryset = Mensagem.objects.all()
    serializer_class = MensagemSerializer
    permission_classes = [IsAuthenticated]
    
    # Diferente do modelo de IA, aqui o filtro é essencial para buscar 
    # as mensagens de uma conversa específica (ex: ?conversa=1)
    filter_backends = [DjangoFilterBackend]
    filterset_class = MensagemFilter

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Se for staff, tem visão total (auditoria)
        if self.request.user.is_staff:
            return qs
            
        # Filtra as mensagens através da relação com a conversa e o usuário
        # "conversa__usuario__user" segue o caminho: Mensagem -> Conversa -> Usuario -> User
        return qs.filter(conversa__usuario__user=self.request.user)

    def perform_create(self, serializer):
    
        # Aqui você pode garantir que o usuário não está tentando enviar uma mensagem
        # para uma conversa que não pertence a ele.
        conversa = serializer.validated_data.get('conversa')
        
        if not self.request.user.is_staff and conversa.usuario.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Você não tem permissão para enviar mensagens nesta conversa.")
            
        serializer.save()




class ConversaViewSet(ModelViewSet):

    queryset = Conversa.objects.all()
    serializer_class = ConversaSerializer
    permission_classes = [IsAuthenticated]
    
    # Adicionando suporte a filtros (ex: filtrar por data ou título)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConversaFilter # Certifique-se de ter essa classe no seu filters.py

    def get_queryset(self):
    
        qs = super().get_queryset()
        
        # Se for administrador da empresa (staff), retorna todas as conversas
        if self.request.user.is_staff:
            return qs
        
        # Se for usuário comum, filtra para retornar apenas as conversas 
        # vinculadas ao perfil do usuário logado.
        # (Considerando que na sua model Conversa existe um campo FK chamado 'usuario')
        return qs.filter(usuario__user=self.request.user)

    def perform_create(self, serializer):
    
        # Busca o perfil do usuário logado
        usuario_perfil = Usuario.objects.filter(user=self.request.user).first()
        serializer.save(usuario=usuario_perfil)





class ModeloIAViewSet(ModelViewSet):

    queryset = ModeloIA.objects.all()
    serializer_class = ModeloIASerializer
    
    # Aqui permitimos que qualquer usuário autenticado veja os modelos,
    # mas você pode restringir a criação/edição apenas para o Admin no futuro.
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
      
        return ModeloIA.objects.all()

    @action(detail=False, methods=['get'], url_path="ativos")
    def modelos_ativos(self, request):
        """
        Uma rota extra caso você queira retornar apenas os modelos 
        que a empresa liberou para uso no momento.
        """
        ativos = self.queryset.filter(ativo=True) # Supondo que exista um campo 'ativo'
        serializer = self.get_serializer(ativos, many=True)
        return Response(serializer.data)
    

