from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.views.generic import ListView
from rest_framework.request import Request
from .serializers import UserSerializer, GroupSerializer, RestaurantSerializer
from .models import Restaurant
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import generics


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class get_restaurants(APIView):
    queryset = Restaurant.objects.all()

    def get(self, request):
        serializer_context = {
            'request': Request(request),
        }

        queryset = Restaurant.objects.all()
        serialized = RestaurantSerializer(queryset, many=True)
        return Response(serialized.data, context=request._request)


def home(request):
    res = Restaurant.objects.all()
    return render(request, 'api/home.html', {'res': res})


class ResView(ListView):
    model = Restaurant
    template_name = 'pins/res.html'
    context_object_name = 'res'


class CreateRes(View):
    def get(self, request):
        name1 = request.GET.get('name', None)
        location = request.GET.get('location', None)
        info = request.GET.get('info', None)

        obj = Restaurant.objects.create(name=name1, location=location, info=info)
        res = {'id': obj.id, 'name': obj.name, 'location': obj.location, 'info': obj.info}

        data = {
            'res': res
        }
        return JsonResponse(data)


def createres(request):
    if request.method == 'POST':
        name1 = request.POST.get('name')
        location1 = request.POST.get('location')
        info1 = request.POST.get('info')

        Restaurant.objects.create(
            name=name1,
            location=location1,
            info=info1
        )
        return HttpResponse('')
    return render(request, 'api/res.html')



class resres(mixins.CreateModelMixin):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)