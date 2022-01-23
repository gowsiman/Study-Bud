from importlib.resources import files
from django.forms import ModelForm, fields
from base.models import Room
from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'