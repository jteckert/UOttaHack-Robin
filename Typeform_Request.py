#import urllib.request
#urllib.request.urlopen("https://api.typeform.com/forms/{form_id}/responses")

import json
import random
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
#print(typeform_info)


for x in range(10):
    priority_num = random.randint(0,3) # demo placeholder for machine learning
    print (priority_num)


items =typeform_info['items']

for item in items:
    answers = item['answers']
    for field in answers:
        print (field['field']['id'])
        if field['field']['id'] == 'LYzGhFItWVze':
            patient_name = field['text']

        #if field['field']['id'] == 'VJCmLdcA5aTJ':
         #   patient_id = field['text']
        
        #print(field['field']['id'])
        #identification = field['id']
        #print(identification)

#print(patient_name)
#print(patient_id)

#totalItemsCounter = typeform_info['total_items']

##iterationsTotal = 500
##iterationsCounter = 0
##timeDelay = 10
##
##while (iterationsCounter < iterationsTotal):
##    iterationsCounter = iterationsCounter + 1
##    
##    typeform_info = get_typeform_info()
##    time.sleep(timeDelay)
##
##
###print (typeform_info)
##
####if typeform_info is not None:
####    print("Here's your info: ")
####    for k, v in typeform_info['account'].items():
####        print('{0}:{1}'.format(k, v))
####
####else:
####    print('[!] Request Failed')
##
##if (totalItemsCounter != typeform_info['total_items']):
    
    
