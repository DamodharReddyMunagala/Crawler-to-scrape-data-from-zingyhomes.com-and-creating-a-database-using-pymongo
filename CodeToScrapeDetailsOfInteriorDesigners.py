import requests
from bs4 import BeautifulSoup
import re
import pymongo
from pymongo import MongoClient as Connection
pages = []

#for page method
firmUrl = []

#for firmProfile method
firmImage = []
name = []
address = []
profile = []
servicesProvided = []
specialty = []
provideServicesIn = []
projects = []
projectGalleryTitleList = []
projectGalleryUrlList = []
projectGalleryImagesUrlsList = []

for i in range(1,192):
    pages.append('http://www.zingyhomes.com/find-interiordesigners/?page=' + str(i) + '&')

def Page(url):
    
    try:
        soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
    except FileNotFoundError:
        req = requests.get(url)
        req.raise_for_status()
        response = open(url.replace('https://','').replace('.','-').replace('/','-') + '.html', 'wb')
        for chunk in req.iter_content(100000):
            response.write(chunk)
        response.close()
        soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
    
    for data in soup.findAll('div', {'class' : 'left-project-profile-detial'}):
        firmUrl.append('http://www.zingyhomes.com' + data.find('a', {'target' : '_blank'}, href = re.compile('^(/interior-designer/)')).attrs['href'])
    

def firmProfile(firmUrl):
    
    try:
        soup = BeautifulSoup(open(firmUrl.replace('/', '').replace('.', '') + '.html'), 'lxml')
    except FileNotFoundError:
        req = requests.get(firmUrl, verify = False)
        response = open(firmUrl.replace('/', '').replace('.', '') + '.html', 'wb')
        for chunk in req.iter_content(100000):
            response.write(chunk)
        response.close()
        soup = BeautifulSoup(open(firmUrl.replace('/', '').replace('.', '') + '.html'), 'lxml')
    
    projectGalleryUrl = []
    projectGalleryTitle = []
    miniProjects = []
    projectGalleryImagesUrls = []
    
    
    try:
        for data in soup.find('section', {'class' : 'list-wrap'}).findAll('section', {'class' : 'tab-nav'}):
            try:
                for item in data.findAll('section', {'class' : 'left-inner-project'}):
                    projectGalleryUrl.append('http://www.zingyhomes.com' + item.find('a', href = re.compile('^(/project-detail/)')).attrs['href'])
            except AttributeError:
                projectGalleryUrl.append('http://zingyhomes.com/')
            try:
                for item in data.findAll('section', {'class' : 'left-inner-project'}):
                    projectGalleryTitle.append(item.find('section', {'class' : 'inner-project-detail'}).find('a', href = re.compile('^(/project-detail/)')).text.replace('\n', '').replace('\t', ''))
            except AttributeError:
                projectGalleryTitle.append('')

            try:
                for item in data.findAll('section', {'class' : 'right-inner-project'}):
                    projectGalleryUrl.append('http://www.zingyhomes.com' + item.find('a', href = re.compile('^(/project-detail/)')).attrs['href'])
            except AttributeError:
                projectGalleryUrl.append('http://zingyhomes.com/')
            try:
                for item in data.findAll('section', {'class' : 'right-inner-project'}):
                    projectGalleryTitle.append(item.find('section', {'class' : 'inner-project-detail'}).find('a', href = re.compile('^(/project-detail/)')).text.replace('\n', '').replace('\t', ''))
            except AttributeError:
                projectGalleryTitle.append('')
    except AttributeError:
        #print (firmUrl.replace('/', '').replace('.', '') + '.html')
        projectGalleryTitle.append('')
        projectGalleryUrl.append('http://zingyhomes.com/')
    
    projectGalleryUrlList.append(projectGalleryUrl)
    projectGalleryTitleList.append(projectGalleryTitle)
    
    try:
        for data in soup.find('section', {'class' : 'contain'}).findAll('section', {'class' : 'left-portfolio-container'}):
            firmImage.append('http://www.zingyhomes.com' + data.find('img').attrs['src'])
    except AttributeError:
        firmImage.append('')
    
    try:
        for data in soup.find('section', {'class' : 'contain'}).findAll('section', {'class' : 'right-portfolio-container'}):
            name.append(data.find('section', {'itemtype' : 'http://schema.org/Person'}).find('h1', {'itemprop' : 'name'}).text.replace('\n', '').replace(' ',''))
    except AttributeError:
        name.append('')
    
    try:
        for data in soup.find('section', {'class' : 'contain'}).findAll('section', {'class' : 'right-portfolio-container'}):
            address.append(data.find('section', {'class' : 'zingy-address-details'}).text.replace('\n','').replace('\xa0','').strip())
    except AttributeError:
        address.append('')
    
    try:
        for data in soup.find('section', {'class' : 'contain'}).findAll('section', {'class' : 'right-portfolio-container'}):
            try:
                profile.append(data.find('section', {'class' : 'zingy-profile-dec'}).find('section', {'id' : 'full-para'}).text.replace('\n', ''))
            except AttributeError:
                profile.append('')
    except AttributeError:
        profile.append('')
    
    try:
        for data in soup.find('section', {'class' : 'contain'}).findAll('section', {'class' : 'right-portfolio-container'}):
            try:
                leftCells = data.find('section', {'class' : 'left-zingyhomes'}).findAll('section', {'class' : 'zingy-profle-tab'})
                middleCells = data.find('section', {'class' : 'middle-zingyhomes'}).findAll('section', {'class' : 'zingy-profle-tab'})
                rightCells = data.find('section', {'class' : 'right-zingyhomes'}).findAll('section', {'class' : 'zingy-profle-tab'})
                if 'Services Provided' in (leftCells[0].text):
                    servicesProvided.append(leftCells[0].find('p').text.replace('\n', ''))
                elif 'Services Provided' in (leftCells[1].text):
                    servicesProvided.append(leftCells[1].find('p').text.replace('\n', ''))
                elif 'Services Provided' in (middleCells[0].text):
                    servicesProvided.append(middleCells[0].find('p').text.replace('\n', ''))
                elif 'Services Provided' in (middleCells[1].text):
                    servicesProvided.append(middleCells[1].find('p').text.replace('\n', ''))
                elif 'Services Provided' in (rightCells[0].text):
                    servicesProvided.append(rightCells[0].find('p').text.replace('\n', ''))
                elif 'Services Provided' in (rightCells[1].text):
                    servicesProvided.append(rightCells[1].find('p').text.replace('\n', ''))
            except AttributeError:
                servicesProvided.append('')
            except IndexError:
                servicesProvided.append('')         
    except AttributeError:
        servicesProvided.append('')
    
    try:
        for data in soup.find('section', {'class' : 'contain'}).findAll('section', {'class' : 'right-portfolio-container'}):
            try:
                leftCells = data.find('section', {'class' : 'left-zingyhomes'}).findAll('section', {'class' : 'zingy-profle-tab'})
                middleCells = data.find('section', {'class' : 'middle-zingyhomes'}).findAll('section', {'class' : 'zingy-profle-tab'})
                rightCells = data.find('section', {'class' : 'right-zingyhomes'}).findAll('section', {'class' : 'zingy-profle-tab'})
                if 'Specialty' in (leftCells[0].text):
                    specialty.append(leftCells[0].find('p').text.replace('\n', ''))
                elif 'Specialty' in (leftCells[1].text):
                    specialty.append(leftCells[1].find('p').text.replace('\n', ''))
                elif 'Specialty' in (middleCells[0].text):
                    specialty.append(middleCells[0].find('p').text.replace('\n', ''))
                elif 'Specialty' in (middleCells[1].text):
                    specialty.append(middleCells[1].find('p').text.replace('\n', ''))
                elif 'Specialty' in (rightCells[0].text):
                    specialty.append(rightCells[0].find('p').text.replace('\n', ''))
                elif 'Specialty' in (rightCells[1].text):
                    specialty.append(rightCells[1].find('p').text.replace('\n', ''))
            except AttributeError:
                specialty.append('')
            except IndexError:
                specialty.append('')         
    except AttributeError:
        specialty.append('')
    
    try:
        for data in soup.find('section', {'class' : 'contain'}).findAll('section', {'class' : 'right-portfolio-container'}):
            try:
                leftCells = data.find('section', {'class' : 'left-zingyhomes'}).findAll('section', {'class' : 'zingy-profle-tab'})
                middleCells = data.find('section', {'class' : 'middle-zingyhomes'}).findAll('section', {'class' : 'zingy-profle-tab'})
                rightCells = data.find('section', {'class' : 'right-zingyhomes'}).findAll('section', {'class' : 'zingy-profle-tab'})
                if 'Provide Services In' in (leftCells[0].text):
                    provideServicesIn.append(leftCells[0].find('p').text.replace('\n', ''))
                elif 'Provide Services In' in (leftCells[1].text):
                    provideServicesIn.append(leftCells[1].find('p').text.replace('\n', ''))
                elif 'Provide Services In' in (middleCells[0].text):
                    provideServicesIn.append(middleCells[0].find('p').text.replace('\n', ''))
                elif 'Provide Services In' in (middleCells[1].text):
                    provideServicesIn.append(middleCells[1].find('p').text.replace('\n', ''))
                elif 'Provide Services In' in (rightCells[0].text):
                    provideServicesIn.append(rightCells[0].find('p').text.replace('\n', ''))
                elif 'Provide Services In' in (rightCells[1].text):
                    provideServicesIn.append(rightCells[1].find('p').text.replace('\n', ''))
            except AttributeError:
                provideServicesIn.append('')
            except IndexError:
                provideServicesIn.append('')         
    except AttributeError:
        provideServicesIn.append('')
    
    for link in projectGalleryUrl:
        projectGalleryImagesUrls.append(ImageGallery(link))
    
    projectGalleryImagesUrlsList.append(projectGalleryImagesUrls)

def ImageGallery(url):
    
    try:
        soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
    except FileNotFoundError:
        req = requests.get(url)
        req.raise_for_status()
        response = open(url.replace('https://','').replace('.','-').replace('/','-') + '.html', 'wb')
        for chunk in req.iter_content(100000):
            response.write(chunk)
        response.close()
        soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
    
    ImageTitle = []
    ImageUrl = []
    ImageUrlList = []
    try:
        for data in soup.findAll('section', {'class' : 'inner-project-details'}):
            try:
                ImageUrl.append('http://www.zingyhomes.com' + data.find('section', {'class' : 'boxgrid'}).find('img', src = re.compile('^(/projectImages/)')).attrs['src'])
            except AttributeError:
                ImageUrl.append('')
    except AttributeError:
        ImageUrl.append('*/*')
            
    for i in range(len(ImageUrl)):
        ImageUrlList.append(ImageUrl[i])
    
    return (ImageUrlList)
        
for url in pages:
    Page(url)


#Page('http://www.zingyhomes.com/find-architects/?page=242&')
for link in firmUrl:
    firmProfile(link)
    
#firmProfile('http://www.zingyhomes.com/architect/sujal-k-s-_30994/')
#ImageGallery('http://zingyhomes.com/')

print (len(firmImage))
print (len(name))
print (len(address))
print (len(profile))
print (len(servicesProvided))
print (len(specialty))
print (len(provideServicesIn))
print (len(projectGalleryUrlList))
print (len(projectGalleryTitleList))
print (len(projectGalleryImagesUrlsList))

connection = Connection()
db = connection.hutstoryZingyHomesInteriorDesigners
firmCollection = db.firms
projectCollection = db.projects
imageGalleryCollection = db.images
for i in range(len(firmUrl)):
    insertFirmData = {"Name" : name[i],
                     "FirmImage" : firmImage[i],
                     "Firm Page" : firmUrl[i],
                     "Profile" : profile[i],
                     "ServicesProvided" : servicesProvided[i],
                     "ProvideServicesIn" : provideServicesIn[i],
                     "Specialty" : specialty[i],
                     "Address" : address[i],
                     "ProjectsPageUrl" : firmUrl[i]}
    FIRMID = firmCollection.insert_one(insertFirmData).inserted_id
    
    for j in range(len(projectGalleryTitleList[i])):
        insertProjectData = {"ProjectImageTitle" : projectGalleryTitleList[i][j],
                            "ProjectImageUrl" : projectGalleryUrlList[i][j],
                            "firmId" : FIRMID}
        PROJECTID = projectCollection.insert_one(insertProjectData).inserted_id
        
        for k in range(len(projectGalleryImagesUrlsList[i][j])):
            insertImageData = {"ImageOfProjectsUrl" : projectGalleryImagesUrlsList[i][j][k],
                              "projectId" : PROJECTID}
            IMAGEID = imageGalleryCollection.insert_one(insertImageData).inserted_id
