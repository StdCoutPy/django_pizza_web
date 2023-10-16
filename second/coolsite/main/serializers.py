from rest_framework import serializers
from .models import P_Menu

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = P_Menu
        fields = ('title',)