##############################################
Authentication
##############################################

By default you can get all the information from Netbox if the login_required option is set to False. If the option is
set to True, you can access the api by username and password to GET the information. The API is only writable if you
have a Token.

* Use the auth_token parameter for the writeable api
* Use the auth parameter to use username and password. The auth parameter is a tuple ('username','password')
