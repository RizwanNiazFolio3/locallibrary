from rest_framework import permissions


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
        elif request.user.groups.filter(name="Librarians"):
            '''
            This checks if the user is part of the librarians group which we defined earlier in one of the tutorials.
            Librarians have access to all the possible request to the api
            '''
            return True
        
        '''
        Users that are not librarians will only be given permissions if they are performing
        One of methods in the SAFE_METHODS attributes. So anonymous users and norml non librarians only get access read operations
        '''
        return False






