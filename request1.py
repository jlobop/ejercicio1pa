import requests;
import sys;

if __name__== '__main__':
    import sys
    print(sys.version_info[0],sys.version_info[1])

    #args={'curso':'api','creador':'jorge', 'nivel':'alto'}
    #url='http://httpbin.org/get'
    url='https://www.google.com'
    url='https://www.brou.com.uy/web/guest/cotizaciones'
    response = requests.get(url)
    if response.status_code == 200:
        #print(response.content)
        file=open('cotizaciones','wb')
        file.write(response.content)
        file.close()
