from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import User

class AddIsLibrarianClaimSerializer(TokenObtainPairSerializer):
    '''
    This class only exists to demonstrate how additional information
    can be added to the payload of a token, allowing us to encode user permissions into the token itself
    '''
    @classmethod
    def get_token(cls, user: User) -> Token:
        token = super().get_token(user)

        # Add custom claims
        if user.groups.filter(name="Librarians"):
            token['isLibrarian'] = True
        else:
            token['isLibrarian'] = False

        return token

class AddIsLibrarianClaimView(TokenObtainPairView):
    '''View used to obtain token pairs'''
    serializer_class = AddIsLibrarianClaimSerializer
