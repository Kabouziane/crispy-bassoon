from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, NoteVersion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class NoteSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    collaborators = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'owner', 'collaborators', 'created_at', 'updated_at']

class NoteVersionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = NoteVersion
        fields = ['id', 'content', 'user', 'created_at']