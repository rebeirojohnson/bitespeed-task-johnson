def identify_user_from_database(email:str,phone_number:str) -> dict:
    
    
    data_to_send_back = {
    "email":email,
    "phoneNumber":phone_number
    }

    return data_to_send_back