import http.client, urllib.request, urllib.parse, urllib.error, base64

def clone_luis_version():
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '{subscription key}',
    }
    
    appId = '51caa2fe-d6c0-4bf3-bd44-3440adf91019'
    versionId = '0.1'
    body = {"version": "0.2"}
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/luis/api/v2.0/apps/{appId}/versions/{versionId}/clone?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
def delete_luis_version():
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '{subscription key}',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("DELETE", "/luis/api/v2.0/apps/{appId}/versions/{versionId}?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))