from rest_framework import viewsets
from ..models import User, Role, Group, Function, Appraisal_format, Appraisal, Session, Topic_present, Criteria
from .serializers import UserSerializer, RoleSerializer, GroupSerializer, FunctionSerializer, SessionSerializer,\
    AppraisalSerializer, AppraisalFormatSerializer, TopicSerializer, CriteriaSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken


'''
Documented Function : convert_fromIDtoName
Programmer(s) : Tu Huynh
Description : Convert from id (primary key) of object to name and
                return attribute __str__ of that object
Parameters : 
- model     : list of model
- fieldName : list of ForeignKey field on the appropriate model
- isList    : True or False
              True used for list
              False used for retrieve
- serializer : serializer of data

Return : 
- serializer.data : data which has been converted from id to __str__
'''
def convert_fromIDtoName(model, fieldName, isList, serializer):
    for num in range(len(model)):
        if isList:
            for i in range(serializer.instance.count()):
                listID = serializer.data[i].get(fieldName[num])
                if listID:
                    if type(listID) is list:
                        if len(listID) != 0:
                            for j in range(len(listID)):
                                listID[j] = str(model[num].objects.get(id=listID[j]))
                    else:
                        serializer.data[i][fieldName[num]] = str(model[num].objects.get(id=listID))
        else:
            listID = serializer.data.get(fieldName[num])
            if listID:
                if type(listID) is list:
                    if len(listID) != 0:
                        for j in range(len(listID)):
                            listID[j] = str(model[num].objects.get(id=listID[j]))
                else:
                    serializer_data = serializer.data
                    serializer_data[fieldName[num]] = str(model[num].objects.get(id=listID))
                    return serializer_data
    return serializer.data

# Custom the ModelViewSet Class with convert the relationship filed from ID to attribute __str__
class CustomModelViewSet(viewsets.ModelViewSet):
    Model = None
    fieldName = None

    def list(self, request, *args, **kwargs):
        Model = self.Model
        fieldName = self.fieldName
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(convert_fromIDtoName(Model, fieldName, True, serializer))

    def retrieve(self, request, *args, **kwargs):
        Model = self.Model
        fieldName = self.fieldName
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(convert_fromIDtoName(Model, fieldName, False, serializer))


class UserViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    Model = [Role, Group]
    fieldName = ['role', 'group']


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class GroupViewSet(CustomModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    Model = [Group]
    fieldName = ['parent_group']


class FunctionViewSet(CustomModelViewSet):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer
    Model = [Role]
    fieldName = ['role']


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic_present.objects.all()
    serializer_class = TopicSerializer


class AppraisalViewSet(CustomModelViewSet):
    queryset = Appraisal.objects.all()
    serializer_class = AppraisalSerializer
    Model = [Session, User, Criteria]
    fieldName = ['session', 'attendee', 'criteria']


class AppraisalFormatViewSet(CustomModelViewSet):
    queryset = Appraisal_format.objects.all()
    serializer_class = AppraisalFormatSerializer
    Model = [Criteria]
    fieldName = ['criteria']


class SessionViewSet(CustomModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    Model = [User, Topic_present, Appraisal_format]
    fieldName = ['presenter', 'topic', 'appraisal_format']


class CriteriaViewSet(viewsets.ModelViewSet):
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer


# API for log-in
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        # renew token if existed
        if Token.objects.filter(user_id=user.id).count() > 0:
            Token.objects.get(user=user).delete()
        token = Token.objects.create(user=user)

        return Response({
            'token': token.key,
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
    })
