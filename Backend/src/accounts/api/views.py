from rest_framework import viewsets
from ..models import User, Role, Group
from .serializers import UserSerializer, RoleSerializer, GroupSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# API for log-in
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if Token.objects.filter(user_id=user.id).count() > 0:
            Token.objects.get(user=user).delete()
        token = Token.objects.create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'full_name': user.get_full_name(),
        })


# API for logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    token = request.auth
    token.delete()
    return Response({"message": "Token has been deleted"})


# API for reset token
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_token(request):
    token = request.auth
    token.delete()
    token = Token.objects.create(user=request.user)
    return Response({
        'token': token.key,
        'user_id': token.user.pk,
        'full_name': token.user.get_full_name(),
    })
