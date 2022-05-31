from multiprocessing import AuthenticationError
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import JSONRenderer
# from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer


User = get_user_model()

# TODO:
# sounds like a custom auth class is the way to go since
# we won't be able to validate via the standard django session as the
# contexts won't line up and we'll always have an Anonymous User here
# so maybe it should be a post call with username in the body?
# otherwise a custom authentication API with X-Username header or some such
# ^^^ or, can we set a session cookie? not sure that will work or how? ^^^
# svelte-kit might play nice here with .locals
# see https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication


class LoginView(APIView):

    # provide a csrf token for allowed/csrf_trusted origins
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response()

    @method_decorator(csrf_protect)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(request.META.get('HTTP_X_CSRFTOKEN'))
        
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                { "message": "Username or Password is Incorrect"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        print(user.is_authenticated)
        login(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserView(APIView):
    # renderer_classes = [JSONRenderer]

    def get(self, request):

        if not request.user.is_authenticated:
            return Response(
                data={"message": "Not Logged In"}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(username=request.user.username).first()
        serializer = UserSerializer(user)
        print(serializer.data)
        # TODO: can we set a session cookie?
        return Response(data=serializer.data, content_type="application/json")


class LogoutView(APIView):
    
    def post(self, request):
        logout(request.user)

        return Response({"message": "success"})
