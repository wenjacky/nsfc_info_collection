#!/usr/bin/env python
# encoding=utf-8

from selenium import webdriver
import pytesseract
from PIL import Image
import requests
import sys 
import time
import pdb

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

ofile = open('countofprojects.txt', "a+")

def save_index(index):
    with open('done.txt','r+') as f:
        f.seek(0)
        f.truncate()
        nu = str(index)
        f.write(nu)

def read_index():
    with open('done.txt','r+') as fi:
        fi.seek(0)
        savedindex = fi.read()
        print ('saved index is:'+savedindex)
        return int(savedindex)



allKeyWords = []
subjectCodeIds = []
years = [] # ['2017', '2016','2015','2014','2013','2012','2011','2010'] # ,'2009','2008','2007','2006','2005']
# grantCodes = ['218','220','222','339','429','432','433','649','579','630','631','632','635','51','52','2699','70','7161']
#grantCodes = ['218','220','222','429','2699','632']
# grantCodes = ['429', '2699']
grantCodes = ['218']
personName = []
personInstitute = []

def restart_firefox(browser):
    print ("restarting firefox...")
    browser.close()
    browser = webdriver.Firefox()
    browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')

def auto_search():
    print('opening a browser...\n')
    alreadydone = read_index()
    browser = webdriver.Firefox()
    browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')
    for s in open("personname.config"):
        personName.append(s[:-1])
    for s in open("personinstitute.config"):
        personInstitute.append(s[:-1])
    
    print (personName, personInstitute)
    i = 0
    for personid in personName:
        if alreadydone > i:
            i += 1
            continue
        
        browser.find_element_by_link_text('人员获资助项目信息查询').click()
        browser.find_element_by_id("resetBt2").click()
        name = unicode(personName[i], errors='replace')
        inis = unicode(personInstitute[i],errors='replace')
        browser.find_element_by_name('psnName_1').send_keys(name)
        browser.find_element_by_name('org_1').send_keys(inis)
        print (i,personid,personInstitute[i])
        browser.find_element_by_id("searchBt2").click()
        result_table = browser.find_element_by_id("grid_2")
        table_trs = result_table.find_elements_by_tag_name("tr")
        for tr in table_trs:
            table_tds = tr.find_elements_by_tag_name("td")
            row = ""
            for td in table_tds:  
                row += td.text + ' '
            ofile.write("result: " + str(i) + ' ' + row +"\n")
        ofile.flush()
        i += 1
        save_index(i)
        #time.sleep(1)
        if (i % 1000 == 0):
            print ("restarting firefox...")
            browser.close()
            browser = webdriver.Firefox()
            browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')
            print ("restart done")

if __name__ == '__main__':
    print("starting...")
    auto_search()
    print("reset index...and exit")
    save_index(0)
