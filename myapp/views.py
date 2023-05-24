from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from myapp.models import Zone,District,State
from myapp.customs.authentications import get_tokens_for_user
from myapp.customs.permission import ZonePermission
from myapp.serializer import LoginSerializer,UserSerializer,ZoneSerializer,DistrictSerializer,StateSerializer
# Create your views here.
class home(APIView):
    def get(self,request):
        return Response({"msg":"no of lines"})
    
class login(APIView):
    authentication_classes = []
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                print("user: ", user)
                user_serializer = UserSerializer(user)
                token = get_tokens_for_user(user)
                response = user_serializer.data
                response["token"] = token
                return Response(response, status=status.HTTP_200_OK)
            return Response(
                {"message": "Invalid Username or Password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ZoneApi(ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def list(self, request, *args, **kwargs):
        zone = Zone.objects.all()
        user = request.user
        if user.has_perm('myapp.view_zone'):
            zone_list = zone
        else:
            zone_list = [i for i in zone if request.user.has_perm('read_obj', i)]
        return Response(ZoneSerializer(zone_list,many=True).data,status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)

class DistrictApi(ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    def list(self, request, *args, **kwargs):
        try:
            district = District.objects.filter(request.data["filter"])
        except:
            return Response({"msg":"filter field require"},status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if user.has_perm('myapp.view_district'):
            district_list = district
        else:
            district_list = [i for i in district if request.user.has_perm('read_obj', i)]
        return Response(DistrictSerializer(district_list,many=True).data,status=status.HTTP_200_OK)

    # permission_classes = [ZonePermission]

class StateApi(ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    # permission_classes = [ZonePermission]
