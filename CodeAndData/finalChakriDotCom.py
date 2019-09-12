# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 20:50:43 2017

@author: Asif
"""
from bs4 import BeautifulSoup

from urllib.request import Request, urlopen
import ErrorHandler as eh
import csv
import codecs
import re
import os.path
import time

fields = ['jobId','industry','noOfVacancy','jobLevel','ageLimit','jobNature','companyName',\
            'experienceReq','position','location','keyRole','salary','date','educationDetails',\
            'jobDetails','othereBenifits']

hdr = {'User-Agent': 'Mozilla/5.0'}

def number_of_row( fileName):
    exist =  os.path.isfile(fileName)
    if exist == True:
        try:
            with open(fileName,"r",encoding='utf-8', errors ='replace') as f:
                reader = csv.reader(f,delimiter = ",")
                data = list(reader)
                row_count = len(data)
                f.close()
        except: 
            row_count=0
    else:
        row_count = 0
    return row_count



def write_list_into_csv(colName,dataList, fileName):
    try:
        numberOfRow = number_of_row(fileName)
        with open(fileName,"a", newline='') as csvfile:
            writer = csv.writer(csvfile)
                
            if numberOfRow == 0:
                writer.writerow(colName)
                                
            for dataRow in dataList:
                #print('\n\ndatarow\n\n',dataRow)
                    
                if  dataRow is not None or len(dataRow) !=0:
                    try:
                        writer.writerow(dataRow)
                    except:
                        print("csv writing problem inside loop")
            
                
        
    except:
        print("csv writing problem")
        
    return




def do_all():
    upperLimit = 99999
    lowerLimit = 51576
    lol = lowerLimit
    upl = upperLimit
    allDataList = []
    while lol <= upl:
        eduDetails = []
        jobInfo = []
        jobDetails = []
        othereBenifits = []
        noOfVacancy = ''
        jobLevel = ''
        ageLimit = ''
        jobNature = ''
        industry = ''
        finalList = []
        jobId = lol
        
        urlid = str(jobId)
        lol += 1
        url = 'http://www.chakri.com/job/show/' + urlid
        responseCode = eh.get_status_code(url)
        if responseCode == 200:
            req = Request(url,headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page,"lxml")
            try:
                date = soup.find("span", class_="dtls_date_posted_job").get_text().strip()
                date = str(date)
            except:
                date = ''
            try:
                companyName = soup.find("p", class_="dtls_company_name").get_text().strip()
            except:
                companyName = ''
            try:
                experienceReq = soup.find("p", class_="dtls_experience").get_text().strip()
            except:
                experienceReq = ''
            try:
                location = soup.find("p", class_="dtls_company_location").get_text().strip()
            except:
                location = ''
            try:
                position = soup.find("div", class_="col-xs-9 col-sm-10 col-md-9").h1.get_text().strip()
            except:
                position = ''
            try:
                keyRole = soup.find("div", class_="dtls_keyskill_container").p.get_text().strip()
            except:
                keyRole = ''
            try:
                salary =  soup.find("p", class_="dtls_salary_text").get_text().strip()
            except:
                salary = ''
            try:
                #print('try')
                jobInfoSoupRight = soup.find_all("div", class_="col-xs-6 col-sm-9 col-md-9 dtls_salary_right_p")             
                jobInfoSoupLeft = soup.find_all("div", class_="col-xs-6 col-sm-3 col-md-3 dtls_salary_left_p")
                rightList = []
                leftList =[]
                for idx, (leftItem, rightItem) in enumerate(zip(jobInfoSoupLeft, jobInfoSoupRight)):
                    tempLeft = str(leftItem)
                    tempLeft = re.sub('<.*?>', '', tempLeft)
                    tempLeft = re.sub('[^A-Za-z0-9 ]+', '', tempLeft)
                    tempLeft = tempLeft.strip()
                    leftList.append(tempLeft)
                    temprRight = str(rightItem)
                    temprRight = re.sub('<.*?>', '', temprRight)
                    #temprRight = re.sub('[^A-Za-z0-9 ]+', '', temprRight)
                    temprRight = temprRight.strip()
                    rightList.append(temprRight)
                
                #print(leftList, rightList)
                for idx, (leftItem, rightItem) in enumerate(zip (leftList, rightList )):
                    #leftItem = leftItem.lower()
                    if leftItem == 'Job Level':
                        jobLevel = rightItem
                    elif leftItem == 'Age Limit':
                        ageLimit = rightItem
                    elif leftItem == 'Job Nature':
                        jobNature = rightItem
                    elif leftItem == 'Industry':
                        industry = rightItem
                    elif leftItem == 'No of Vacancies':
                        noOfVacancy = rightItem
                    
                #print(jobLevel,'\n',ageLimit, '\n' ,jobNature,'\n',industry,'\n',noOfVacancy)
                '''
                for element in jobInfoSoup:
                    jobInfo.append(element.get_text().strip())
                noOfVacancy = jobInfo[0]
                jobLevel = jobInfo[1]
                ageLimit = jobInfo[2]
                jobNature = jobInfo[3]
                industry = jobInfo[4]
                '''
            except:
                print('error in important...')
            try:
                
                jobDetailsSoup = soup.find("div", class_="job_details_left_container").find_all('li')
                #print(jobDetailsSoup)
                
                for element in jobDetailsSoup:
                    jobDetails.append(element.get_text())
                jobDetails = list(filter(None,jobDetails))
                jobDetails = '  \n  '.join(jobDetails)
                #print(len(jobDetails))
                
                #print((jobDetails))
            except:
                #print('no...job details')
                jobDetails = []
                
            try:
                
                educationAndOtherBenifits = soup.find_all("div", class_="dtls_education_required")
                listOfEduOtherBen = []
                #print(len(educationAndOtherBenifits))
                for item in educationAndOtherBenifits:
                    tempStr = str(item)
                    tempStr = re.sub('<.*?>', ' <tag> ', tempStr)
                    tempList = tempStr.split(" <tag> ")
                    for sent in tempList:
                        sent = sent.strip()
                        if(len(sent)>0):                            
                            listOfEduOtherBen.append(sent)
                
                idxOfEdu = listOfEduOtherBen.index('Desired Education')
                idxOfOB = listOfEduOtherBen.index('Other Benefits')
                if idxOfEdu > idxOfOB:
                    eduDetails = listOfEduOtherBen[idxOfEdu+1 : ]
                    othereBenifits = listOfEduOtherBen[idxOfOB+1 : idxOfEdu]
                else:
                    othereBenifits = listOfEduOtherBen[idxOfOB+1 : ]
                    eduDetails = listOfEduOtherBen[idxOfEdu+1 : idxOfOB]
                   
                eduDetails = '\n'.join(eduDetails)
                othereBenifits = '\n'.join(othereBenifits)
                #print(eduDetails, '\n\n\n\n\n\n\n\n',othereBenifits)
                '''
                
                for element in education:
                    findP = element.find_all('p')
                    for p in findP:
                        eduDetails.append(p.get_text())
                eduDetails = list(filter(None, eduDetails))
                #print(eduDetails)
                for element in education:
                    
                    findLi = element.find_all('li')
                    print('findli-=',findLi)
                    for li in findLi:                        
                        othereBenifits.append(li.get_text())
                othereBenifits = list(filter(None, othereBenifits))
                if(len(eduDetails)==0):
                    eduDetails.append(othereBenifits[0])
                    othereBenifits = othereBenifits[1:]
                if(len(othereBenifits)==0):
                    othereBenifits.append(eduDetails[0])
                    eduDetails = eduDetails[1:]
                    print('\n\nother\n\n', othereBenifits)
                if(len(eduDetails)>=1):
                    eduDetails = ' '.join(eduDetails)
                if(len(othereBenifits)>=1):
                    othereBenifits = ' '.join(othereBenifits)
                '''
            
            except:
                print('no edu other')
                    
            finalList = [jobId,industry,noOfVacancy,jobLevel,ageLimit,jobNature,\
            companyName, experienceReq, position, location, keyRole, salary,\
            date, eduDetails, jobDetails, othereBenifits]  
            #print(finalList)
            allDataList.append(finalList)
            #print(date,'\n',companyName,'\n',location,'\n',noOfVacancy)
            #print(othereBenifits,'\n\n\n\n\n',eduDetails)
                
                
    #now write lists in csv file
    #numOfRow = number_of_row('ChakriDotCom.csv')
        if len(allDataList)>0:
            write_list_into_csv(fields, allDataList, 'ChakriDotCom.csv' )
            allDataList = []
        print('jobID->',jobId) 
        #time.sleep(4)

                
do_all()                
                
                
                
                
                
                
                
                
                
                
        
    