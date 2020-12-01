from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import BookSerializer, AuthorSerializer, PlaceSerializer, RentSerializer, CustomerSerializer, \
    UserSerializer
from .models import Book, Author, Customer, Place, Rent
from django.contrib.auth.models import User
from .permissions import IsAuthenticatedOrPostOnly
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Book'])
class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer


@extend_schema(tags=['Author'])
class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Author.objects.all().order_by('first_name')
    serializer_class = AuthorSerializer


@extend_schema(tags=['Place'])
class PlaceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Place.objects.all().order_by('postcode')
    serializer_class = PlaceSerializer


@extend_schema(tags=['Customer'])
class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Customer.objects.all().order_by('first_name')
    serializer_class = CustomerSerializer


@extend_schema(tags=['Rent'])
class RentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Rent.objects.all().order_by('-begin')
    serializer_class = RentSerializer


@extend_schema(tags=['User'])
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrPostOnly]

    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
