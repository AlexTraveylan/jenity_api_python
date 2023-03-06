from django.http import HttpRequest
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jenity.models import Channel, Message, UserApp, CookieApp
from jenity.serializers import ChannelSerializer, MessageSerializer, UserAppSerializer, CookieSerializer

# Channel
class ChannelViewSet(ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


# Message
class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def get_queryset(self):
        channelId = self.request.GET.get('channel_id')
        if channelId:
            set = self.queryset.filter(channel_id = channelId)
            return set
        else:
            return self.queryset

# User
class UserAppViewSet(ModelViewSet):
    queryset = UserApp.objects.all()
    serializer_class = UserAppSerializer


# Cookie
class CookieViewSet(ModelViewSet):
    queryset = CookieApp.objects.all()
    serializer_class = CookieSerializer


# Login
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try :
            username: str = request.data["username"]
            password: str = request.data["password"]
            user: UserApp = UserApp.objects.get(username = username, password = password)

            if user.cookie:
                user.cookie.delete()

            cookie = CookieApp.objects.create()
            user.cookie = cookie
            user.isLogged = True
            user.save()
            return Response({'message' : 'Vous êtes connecté', 'user': {
                'username': user.username,
                'cookie': user.cookie.sessionId if user.cookie else None
            }}, status=status.HTTP_200_OK)
        except:
            return Response({'message': "Bad credentials"}, status=status.HTTP_404_NOT_FOUND)


# logout
class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            username: str = request.data["username"]
            sessionID: str = request.data["sessionId"]

            user = UserApp.objects.get(username = username)
            if user.cookie.sessionId == sessionID:
                cookie = CookieApp.objects.get(sessionId = sessionID)
                print(cookie)
                cookie.delete()
                print(user)
                return Response({"message" : "Vous avez bien été déconnecté"}, status=status.HTTP_200_OK)
            else:
                return Response({'message' : "Vous ne pouvez pas deconnecter cet utilisateur"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message' : "Vous ne pouvez pas deconnecter cet utilisateur"}, status=status.HTTP_401_UNAUTHORIZED)
