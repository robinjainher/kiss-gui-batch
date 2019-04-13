import bs4,requests,os

names = os.listdir()
b = []
for name in names:
    if('_RV.txt' in name):
        b.append(name)

for i in range(len(b)):
    print(str(i) + '  ' + b[i])

choice = int(input('Enter Choice : '))
name = b[choice]

#name = 'kono-koi-wa-tsumi-na-no-ka'
#name = input("Enter FileName : ")
quality = int(input("Enter Quality (0=480p,1=720p,2=1080p)"))
#def start():
file = open(name,'r')
a= file.read()
list2 = list(a.split('\n'))
file.close()

list_3 = []
list_4 = []

for url in list2:
    res = requests.get(url)
    if (str(res)!='<Response [404]>'):
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,features="lxml")
        elem = soup.select('a#button-download')
        elem1= soup.select('strong')
        print(f"Downloading {elem1[0].text}") 
        try:
            list_3.append(elem[quality].get('href'))
            list_4.append(elem1[0].text)
        except:
            try:
                list_3.append(elem[quality-1].get('href'))
                list_4.append(elem1[0].text)
            except:
                try:
                    list_3.append(elem[quality-2].get('href'))
                    list_4.append(elem1[0].text)
                except:
                    print("Error "+url)
    else:
        print('404 Not Found '+url)
name = name.split('_')[0]
file = open(name+'_url.txt','w')
str3 = '\n'.join(list_3)
file.write(str3)
file.close()
file = open(name+'_N.txt','w')
str4 = '\n'.join(list_4)
file.write(str4)
file.close()
#start()

