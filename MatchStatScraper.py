def websiteExtracter():
    import bs4
    from bs4 import BeautifulSoup
    import requests
   
    webpage = "https://www.skysports.com/premier-league-results/2019-20"
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    webPage = requests.get(webpage, headers = headers).text
    soup = BeautifulSoup(webPage, 'lxml')
    links=[]
    for link in soup.find_all('a',class_ = 'matches__item matches__link'):
        links.append(link.get('href'))
    return(links[0:50])
def MatchDet(webpage):
    import bs4
    from bs4 import BeautifulSoup
    import requests
    import csv
    Score=[]
    Match=""
    Datalist=[]
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    webPage = requests.get(webpage, headers = headers).text
    soup = BeautifulSoup(webPage, 'lxml')
    for header in soup.find_all('div', class_ = 'sdc-site-match-header__detail'):
        MatchDet=(header.find('p', class_ = 'sdc-site-match-header__detail-fixture').text.strip())
        MatchName=(" ".join(MatchDet.split())).split('.')[0]
        Competition=(" ".join(MatchDet.split())).split('.')[1]
        time=(header.find('time', class_ = 'sdc-site-match-header__detail-time').text.strip())
        Venue=(header.find('span', class_ = 'sdc-site-match-header__detail-venue').text.strip()).replace(',','.')
    for tag in soup.find_all('span', class_ = 'sdc-site-match-header__team-name-block-target'):
        Match=Match+(tag.text.strip())+","
    for S_tag in soup.find_all('span', class_ = 'sdc-site-match-header__team-score-block'):
        Score.append(int(S_tag.text.strip()))
    for G_tag in soup.find_all('span', class_ = 'sdc-site-match-header__team-score-block'):
        Score.append(int(G_tag.text.strip()))
    Cards=""
    Goals=soup.find_all('ul', class_ = 'sdc-site-match-header__team-synopsis')[0].text.strip()
    HomeEvent=(" ".join(Goals.split()).replace(',','.'))
    Events=(" ".join(Goals.split())).split(')')
    Events.pop(-1)
    HomeScorers=""
    Cards=""
    for event in Events:
        if (event.find('sent off')==-1):
            HomeScorers=HomeScorers+event+"):"
        else:
            Cards=Cards+event+"):"
    Goals=soup.find_all('ul', class_ = 'sdc-site-match-header__team-synopsis')[1].text.strip()
    AwayEvent=(" ".join(Goals.split()).replace(',','.'))
    Events=(" ".join(Goals.split())).split(')')
    Events.pop(-1)
    AwayScorers=""
    for event in Events:
        if (event.find('sent off')==-1):
            AwayScorers=AwayScorers+event+"):"
        else:
            Cards=Cards+event+"):"
    if Cards=="":
        Cards="No Suspensions"
    print(MatchName)
    Line=MatchName+","+Competition+","+time+","+Venue+","+Match+str(Score[0])+","+str(Score[1])+","+(HomeScorers.replace(',','.'))+","+(AwayScorers.replace(',','.'))+","+Cards+","+HomeEvent+","+AwayEvent
    Datalist.append(Line.split(','))
    with open("Data/"+Competition+".csv", "a",errors='ignore') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in Datalist:
            writer.writerow(line)

a=websiteExtracter()
for page in range(len(a)):
    MatchDet(a[page])