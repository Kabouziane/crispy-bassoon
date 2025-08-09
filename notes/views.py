from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db import models
from .models import Note, NoteVersion
from .serializers import NoteSerializer, NoteVersionSerializer, UserSerializer

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(
            models.Q(owner=self.request.user) | 
            models.Q(collaborators=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_collaborator(self, request, pk=None):
        note = self.get_object()
        if note.owner != request.user:
            return Response({'error': 'Only owner can add collaborators'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            note.collaborators.add(user)
            return Response({'message': 'Collaborator added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        note = self.get_object()
        versions = note.versions.all()[:10]  # Last 10 versions
        serializer = NoteVersionSerializer(versions, many=True)
        return Response(serializer.data)