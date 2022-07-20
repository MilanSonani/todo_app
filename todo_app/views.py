from .serializers import CreateBookSerializer, UpdateBookSerializer, UserRegisterSerializer,\
     LoginResponseSerializer, LoginRequestSerializer, ChangePasswordSerializer,\
         BookResponseSerializer, UpdateBookSerializer
from .models import User, Book
from .permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permisssion_classes = (AllowAny,)
    parser_classes = [MultiPartParser]

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.role == "LIBRARIAN":
            user.is_staff = True
            user.save()
        response = LoginResponseSerializer(user, context=self.get_serializer_context())
        return Response(response.data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginRequestSerializer
    permisssion_classes = (AllowAny,)
    parser_classes = [MultiPartParser]

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        response = LoginResponseSerializer(user, context=self.get_serializer_context())
        return Response(response.data, status=status.HTTP_201_CREATED)


class AddBookView(generics.CreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CreateBookSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        response = BookResponseSerializer(book, context=self.get_serializer_context())
        return Response(response.data, status=status.HTTP_201_CREATED)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()


class UpdateBookView(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def put(self, request, pk, format=None):
        book_obj = get_object_or_404(Book, pk=pk)
        serializer = UpdateBookSerializer(book_obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBookView(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def delete(self, request, pk, format=None):
        book_obj = get_object_or_404(Book, pk=pk)
        book_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetailBookView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Book.objects.all()
    serializer_class = BookResponseSerializer


class ListBookView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Book.objects.all()
    serializer_class = BookResponseSerializer

