from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
JWT_authenticator = JWTAuthentication()


#Creating our own custom permission to allow only users in the librarian group to perfrom CRUD operations
class IsLibrarian(permissions.BasePermission):

    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            '''
            This overides the has_permission method of the BasePermission class.
            The method first checks if the method request is in SAFE_METHODS attribute of the permissions class
            The SAFE_METHOD attribute is a tuple of the form ('GET','HEAD','OPTION') that checks
            if the method of the request is one of the "safe" read operations.
            basically, if the user is performing a GET, HEAD, or OPTION request then they have the permission to do so
            '''
            return True
        else:
            response = JWT_authenticator.authenticate(request)
            if response is not None:
                # unpacking, we only need the token
                _ , token = response
                #Checking if the token mentions that the user is librarian
                librarian_status = token.payload['isLibrarian']
                '''
                Since tokens are only active for 5 minutes,
                It is possible that within the time the token was created the user is no longer a librarian.
                '''
                if librarian_status == True:
                    if request.user.groups.filter(name="Librarians"):
                        return True      
        return False

class OnlyLibrarians(permissions.BasePermission):
    def has_permission(self,request,view):
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking, we only need the token
            _ , token = response
            #Checking if the token mentions that the user is librarian
            librarian_status = token.payload['isLibrarian']
            '''
            Since tokens are only active for 5 minutes,
            It is possible that within the time the token was created the user is no longer a librarian.
            '''
            if librarian_status == True:
                if request.user.groups.filter(name="Librarians"):
                    return True
        return False




