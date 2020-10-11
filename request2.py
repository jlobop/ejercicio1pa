import requests;


if __name__== '__main__':


    #args={'curso':'api','creador':'jorge', 'nivel':'alto'}
    #url='http://httpbin.org/get'
    url='https://www.google.com'
    url='https://www.brou.com.uy/web/guest/cotizaciones'
    userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    headers={'User-Agent':userAgent}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        #print(response.content)
        file=open('cotizaciones','wb')
        file.write(response.content)
        file.close()
