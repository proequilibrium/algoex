import httplib2

from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow


# Copy your credentials from the console
CLIENT_ID = '111600650766547016717'
CLIENT_SECRET = r'"private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCZRVld3Y0XVtJ/\nSd5ct/2smV5Ns8iqhOAIfe3uPAEbBsHX5CxvdD2ITZ/2up02tPwbww1s1T3J0RA2\nOUCy6kdFwfu0No5dyK57bn8XH3Ol9HLyMcqnrPcvq4FpytB5tq6/C/0FdI7XeqRp\nGnwXVK72KsSq6XSfNsWyKIZJHu+DE/0otDBCjg3NW0YyIFphpqMH6HGOhnDr9Gd5\nY3bb5b2Bge/7Tw8xritlKflcMjiIHgu+Zu9D8dmwWWvd1qJKSO74VjjwxrrpAIUg\n9Vjq/IeYRT6weiLJhV7M6YJEqZAQfvlj04VDF7McvyR7lXgKzr2Jn0mfVYF4InNI\n8npBvuUhAgMBAAECggEACrmpmUHpn5p5vGKE5uQRIkTRLorIHfaSXsXBIoycXzHH\n2r2ixmHR9HnKGc/RNITRp3esttLtMfQpOEIlXt+6AQ2j+WZf6/whCY4f4pRW2WQT\nrxMA5V7bJUDRG4APupSoAcJrADi5ziZM3vX1fQR2Ac/YV0Vi3clNaDwhuXgqtndR\n20fZdQ/isSCIMpmRo1W4L3ua4kVGmJ7Pgc/VIbtWI9KQYyguN3+eOYEJd7FF6AMT\nVW82BL9gvnrHSR6am1XLFQjC3OMdkZadQuVleFU8vKFELAOu9tGpB1C/ozkAhq4J\nsxjWqxZWDy1KB2ELYJLoZN9OgiM4vqaJqHO7Slo94QKBgQDQnRAmHQg4Io9jOTWs\nyhLS4iZKl034OAZjntMiXBocbuEBJjHrwIWkc9u13PtUSubHMvQ5fizswhIRpn7m\nBFYJFSdWfsuqBDfSSldVtK9I4vDkwU/3i339UBYfZRNy4liqbd4PC7sxAibZlLVE\n6hB0HEPTOg+JGwedbIFmd7DR3QKBgQC8FhiODx53RXeFdoeGWsRnsW/Zmm92svVD\nyoYeJx+0Uo+6YBQ962r4iJ/u1HgdN7DF6WwKvGzBSS8G73M3Fc7QSz6FPfStRJB+\ngSw6C2QSgTEG6UFyqp+sAuw6y3RpVt5G2+psD49am+pIobVJQTdBShgs9vvmnpF+\n8lun77SGFQKBgGTayifi+UpKSxApZG249AjIFMMTCzrpuw0GiASgim8cm+M2WAQl\n+3ZaHOp7f3ZtD81WMQRqn8WGvb2SxN7nUcDqXS5P9p6nk2UzU623wNZ4AQZW/xYq\ndiq1QTzEXPa5vywGGckkXsd+xtGCN3CtyG6aC6Be/YvHaZMOFjE3xGBxAoGBAKis\nlCbKDkNeS/qnupBV1C895BXctrtXcDb0Z+Sgp4EaTYUR5vVEq3DpbaxMZM+nAuPq\nGpdiNZH9ZKwujz/GUetgn1f0oPnGNGMOyq/fSUaDD4moI6aGt50WHe34SZSyb7JS\nRF/WcHQMwUWTp7VjQ/9MSHQCpxNB/y8+f84SXO2lAoGAOXIzDWIYzZxY0jVn+tvV\nghWFEMzRMz9rQ5hUvHHGiSwzvqPLRQ90SKfIiKNAzNFkqeE/2BbVNEXgNqGZAuy8\n9jR2AkDMlDVyeU0OD7Pr5RkkiLwOWx+TWZh1o9hoyC51g4X8wO8Do44iddDHBiox\ndBMih0zBkd0UQPxkjP/sK4E=\n-----END PRIVATE KEY-----\n'

# Check https://developers.google.com/webmaster-tools/search-console-api-original/v3/ for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print('Go to the following link in your browser: {}'.format(authorize_url))
code = input('Enter verification code: ')
credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

webmasters_service = build('webmasters', 'v3', http=http)

# Retrieve list of properties in account
site_list = webmasters_service.sites().list().execute()

# Filter for verified websites
verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry']
                       if s['permissionLevel'] != 'siteUnverifiedUser'
                          and s['siteUrl'][:4] == 'http']

# Printing the URLs of all websites you are verified for.
for site_url in verified_sites_urls:
  print(site_url)
  # Retrieve list of sitemaps submitted
  sitemaps = webmasters_service.sitemaps().list(siteUrl=site_url).execute()
  if 'sitemap' in sitemaps:
    sitemap_urls = [s['path'] for s in sitemaps['sitemap']]
    print ("  " + "\n  ".join(sitemap_urls))
