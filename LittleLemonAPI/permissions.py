from rest_framework import permissions

class CustomPermissions(permissions.BasePermission):
 def has_permissions(self,request,view):
  if not request.user.is_authenticated:
   return False