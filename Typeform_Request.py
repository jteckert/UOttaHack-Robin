#import urllib.request
#urllib.request.urlopen("https://api.typeform.com/forms/{form_id}/responses")

import json
import requests

api_token = 'AJfMdhh29KazXMzpjNDo2c1VAaTxyoQ8C3zwuYYEM4mG'
api_url_base = 'https://api.typeform.com/'
api_form_id = 'sINTqV'

headers = {'Authorization': 'Bearer {0}'.format(api_token)}

def get_typeform_info():

    #https://api.typeform.com/forms/{form_id}/responses
    api_url = '{0}/forms/{1}/responses'.format(api_url_base, api_form_id)
    #api_url = 'https://api.typeform.com/forms/sINTqV/responses'
    

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


typeform_info = get_typeform_info()

print (typeform_info)

##if typeform_info is not None:
##    print("Here's your info: ")
##    for k, v in typeform_info['account'].items():
##        print('{0}:{1}'.format(k, v))
##
##else:
##    print('[!] Request Failed')

parsed_json = json.loads(typeform_info)

