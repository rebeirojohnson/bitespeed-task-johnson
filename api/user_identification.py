import json
from api import dbcon


def identify_user_from_database(email: str, phone_number: str) -> dict:

    if phone_number is not None and email is not None:
        query = f"""SELECT * FROM public.contact
            where email = %(email)s or "phoneNumber" = (select "phoneNumber" from public.contact where email = %(email)s) or "phoneNumber"=%(phoneNumber)s or email = (select email from public.contact where "phoneNumber"=%(phoneNumber)s )
            ORDER BY id ASC """

    elif phone_number is None:
        query = f"""SELECT * FROM public.contact
            where "phoneNumber" = %(phoneNumber)s or email = (select email from public.contact where "phoneNumber" = %(phoneNumber)s)
            ORDER BY id ASC """

    elif phone_number is None:
        query = f"""SELECT * FROM public.contact
            where email = %(email)s or "phoneNumber" = (select "phoneNumber" from public.contact where email = %(email)s)
            ORDER BY id ASC """

    df = dbcon.processquery(
        query=query, args={"email": email, "phoneNumber": phone_number}
    )

    df_json = df.to_json(orient='records')
    
    data_to_send_back = json.loads(df_json)

    return data_to_send_back
