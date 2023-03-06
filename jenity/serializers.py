from rest_framework.serializers import ModelSerializer

from jenity.models import Channel, UserApp, Message, CookieApp


class ChannelSerializer(ModelSerializer):

    class Meta:
        model = Channel
        fields = '__all__'


class UserAppSerializer(ModelSerializer):

    class Meta:
        model = UserApp
        fields = '__all__'


class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
    
class CookieSerializer(ModelSerializer):

    class Meta:
        model = CookieApp
        fields = '__all__'
    
