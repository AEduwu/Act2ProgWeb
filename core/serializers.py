from rest_framework import serializers
from .models import USER, GAME

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = USER
        fields = '__all__'
        
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GAME
        fields = '__all__'