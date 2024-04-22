import json
from api import dbcon


def identify_user_from_database(email: str, phone_number: str) -> dict:

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

    df = dbcon.processquery(
        query=query, args={"email": email, "phoneNumber": phone_number}
    )
    
    
    df_json = json.loads(df.to_json(orient='records'))
    

    primary_row = df.loc[df['linkPrecedence'] == 'primary']['id']
    
    if len(primary_row) == 1:
        primaryContatctId = primary_row[0]

        phone_num_list_list = df['phoneNumber'].to_list()
        
        email_list = df['email'].to_list()
            
    print(primary_row)
    
    data_to_send_back = {
		"contact":{
			"primaryContatctId": primaryContatctId,
			"emails": email_list,
			"phoneNumbers": phone_num_list_list,
			"secondaryContactIds": [23]
		}
	}

    return data_to_send_back

def insert_user(phoneNumber, email, linkedId, linkPrecedence):
    pass