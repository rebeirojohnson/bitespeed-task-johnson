import json
from api import dbcon

def get_query_based_on_condition(email: str, phone_number: str):
    if phone_number is not None and email is not None:
        query = f"""SELECT * FROM public.contact
            where email = %(email)s or "phoneNumber" = (select "phoneNumber" from public.contact where email = %(email)s limit 1)  or "phoneNumber"=%(phoneNumber)s or email = (select email from public.contact where "phoneNumber"=%(phoneNumber)s limit 1 )
            ORDER BY contact."linkPrecedence" ASC """

    elif phone_number is None:
        query = f"""SELECT * FROM public.contact
            where "phoneNumber" = %(phoneNumber)s or email = (select email from public.contact where "phoneNumber" = %(phoneNumber)s limit 1)
            ORDER BY contact."linkPrecedence" ASC """

    elif phone_number is None:
        query = f"""SELECT * FROM public.contact
            where email = %(email)s or "phoneNumber" = (select "phoneNumber" from public.contact where email = %(email)s limit 1)
            ORDER BY contact."linkPrecedence" ASC """
    else:
        raise Exception("Either Email or Phone Number must be passed")
    
    return query 

def identify_user_from_database(email: str, phone_number: str) -> dict:

    query = get_query_based_on_condition(email=email,phone_number=phone_number)
    

    df = dbcon.processquery(
        query=query, args={"email": email, "phoneNumber": phone_number}
    )
    
    if df.empty:
        insert_user(phoneNumber=phone_number,email=email,linkPrecedence='primary')
        
        df = dbcon.processquery(
        query=query, args={"email": email, "phoneNumber": phone_number}
        )
        
    primary_row = df.loc[df['linkPrecedence'] == 'primary']['id']
    
    print(primary_row)
    
    if len(primary_row) == 1:
        
        
        primaryContatctId = primary_row[0]

        phone_num_list_list = df['phoneNumber'].to_list()
        
        phone_num_list_list = filter_list(phone_num_list_list)
        
        email_list = df['email'].to_list()
        
        email_list = filter_list(email_list)
            

        data_to_send_back = {
            "contact":{
                "primaryContatctId": primaryContatctId,
                "emails": email_list,
                "phoneNumbers": phone_num_list_list,
                "secondaryContactIds": [23]
            }
        }

        return data_to_send_back
    elif len(primary_row) > 1:
        print(df)
        raise Exception ("Multiple match conditions found")

def insert_user(phoneNumber, email, linkPrecedence):
    insert_data_query = """INSERT INTO public.contact(
	 "phoneNumber", email, "linkedId", "linkPrecedence")
	VALUES (%(phoneNumber)s, %(email)s, (select id from public.contact where email = %(email)s or "phoneNumber" = %(phoneNumber)s), %(linkPrecedence)s) returning id;"""
    
    vars = {
        "phoneNumber":phoneNumber,
        "email":email,
        "linkPrecedence":linkPrecedence
    }
    

    new_id = dbcon.excute_query(query=insert_data_query,args=vars)
    
    return new_id

def filter_list(unflitered_list):
    filtered_list = [x for x in unflitered_list if x is not None]

    temp_list = set()
    # Filter out repeated elements
    filtered_list = [x for x in unflitered_list if x is not None and not (x in temp_list or temp_list.add(x))]
    
    return filtered_list