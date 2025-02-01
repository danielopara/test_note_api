from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Notes, User, UserProfile
from .serializers import NoteSerializer, UserProfileSerializer, UserSerializer


# Create your views here.
class NoteView():
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_notes(request):
        notes = Notes.objects.all()
        serializer = NoteSerializer(notes, many=True)
        response_data = {
            'length' :  notes.count(),
            'data': serializer.data
        }
        return Response(response_data, status = status.HTTP_200_OK)

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def create_note(request):
        data = request.data.copy()
        # data['updated_at']= None
        data['user'] = request.user.id
        note = NoteSerializer(data = data)
        if note.is_valid():
            saved_note =note.save()
            return Response(NoteSerializer(saved_note).data, status=status.HTTP_201_CREATED)
        return Response(note.errors, status= status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_note_by_id(request, id):
        try:
            note = Notes.objects.get(id=id)
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Notes.DoesNotExist:
            return Response({'message': "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        
    
    @api_view(['PATCH', 'PUT'])
    @permission_classes([IsAuthenticated])
    def patch_note(request, id):
        try:
            note = Notes.objects.get(id=id)
            
            partial = request.method == 'PATCH'
            serializer = NoteSerializer(note, data=request.data, partial=partial)
            if serializer.is_valid():
                updated_note = serializer.save()
                return Response(NoteSerializer(updated_note).data, status=status.HTTP_200_OK )
        except Notes.DoesNotExist:
            return Response({'message': "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        
class UserView():
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def register_user(request):
        if User.objects.count() > 1: 
            return Response({'message': "Rest"}, status=400)
        
        user_serializer = UserSerializer(data=request.data.get('user'))
        profile_serializer = UserProfileSerializer(data=request.data)
        
        is_user_valid = user_serializer.is_valid()
        is_profile_valid = profile_serializer.is_valid()
        
        if not is_user_valid or not is_profile_valid:
            return Response({'user_error': user_serializer.errors, "profile_error": profile_serializer.errors}, status=400)
        
        
        user = user_serializer.save()
        user.set_password(request.data['user']['password'])
        user.save()
            
        profile = UserProfile.objects.create(user=user, phone=request.data['phone'])
            
        return Response({'profile':UserProfileSerializer(profile).data, 'user':UserSerializer(user).data}, status=200)
    
    @api_view(['POST'])
    def login(request):
        username = request.data['username']
        password = request.data['password']
        
        if not username or not password:
            return Response({'message': "username and password are required"}, status=400)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return Response({'access_token': access_token, 'refresh_token': str(refresh)}, status=200)
        return Response({'message': "Invalid credentials"}, status=400)
