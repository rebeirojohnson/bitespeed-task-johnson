from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.user_identification import identify_user_from_database

@api_view(['GET','POST'])
def index_view(request):

    try:
        email = request.data.get('email',None)
        
        phone_number = request.data.get('phoneNumber',None)

        data_to_send_back = identify_user_from_database(email=email,phone_number=phone_number)
        
        response = Response(data_to_send_back)

        return response
    except Exception as e:
        
        data_to_send_back = {
            "message":"error",
            "error":str(e)
        }

        response = Response(data_to_send_back,status=500)

        return response