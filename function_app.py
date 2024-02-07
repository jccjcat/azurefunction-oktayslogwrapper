import azure.functions as func
import os
import requests
import logging

app = func.FunctionApp()

@app.function_name(name="GetSysLog")
@app.route(route="logs", auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request to get Okta log.')

    # Retrieve SSWS token and Okta domain from environment variables
    ssws_token = os.environ.get('OKTA_SSWS_TOKEN')
    okta_domain = os.environ.get('OKTA_DOMAIN')

    if not ssws_token or not okta_domain:
        return func.HttpResponse(
             "Please ensure your Okta SSWS token and domain are configured.",
             status_code=400
        )

    # Retrieve query string parameters
    filter_param = req.params.get('filter')
    
    # Prepare the request to Okta Systems Log API
    url = f'{okta_domain}/api/v1/logs'
    headers = {'Authorization': f'SSWS {ssws_token}'}
    
    # Include query parameters if available
    params = {}
    if filter_param:
        params['filter'] = filter_param

    # Send the request to Okta
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # Forward the Okta API response
        return func.HttpResponse(response.text, mimetype="application/json")
    else:
        # Forward any error responses from Okta
        return func.HttpResponse(response.text, status_code=response.status_code)