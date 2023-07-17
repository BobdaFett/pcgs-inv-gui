from office365.graph_client import GraphClient

import msal

def get_user_cert():
    app = msal.PublicClientApplication(
        
    )