#!/usr/bin/env python
# encoding=utf-8

"""
NSFC AutoQuery.

Usage:
  auto_search.py [-g | -p] [--subjectfile=] [--yearfile=] [--keywordfile=] [--grantfile=] [--personnamefile=] [--personinstitutefile=]
  auto_search.py (-h | --help)
  auto_search.py --version

Options:
  -g --gerernalquery                    run in gerneral query mode.
  -p --projectcount                     run in project count mode.
  --subjectfile=<filename>              specify the subject config file [default: subject.config].
  --yearfile=<filename>                 specify the year config file [default: year.config].
  --keywordfile=<filename>              specify the keyword file [default: keyword.config].
  --grantfile=<filename>                specify the grant config file [default: grant.config].
  --personnamefile=<filename>           specify the personname config file [default: personname.config].
  --personinstitutefile=<filename>      specify the personinstitute config file [default: personinstitute.config].
  --donefile=<filename>                 specify the done config file [default: done.config].
  -h --help                             Show help information.
  --version                             Show version.

"""

from docopt import docopt
from selenium import webdriver
import pytesseract
from PIL import Image
#import requests
import sys 
import time
import pdb
import logging
from logging.handlers import TimedRotatingFileHandler
from docopt import docopt

subjectfile = "subject.config"
yearfile = "year.config"
keywordfile = "keyword.config"
grantfile = "grant.config"
personnamefile = "personname.config"
personinstitutefile = "personinstitute.config"
donefile = "done.config"

#keywords        
allKeyWords = []

#subject code
subjectCodeIds = []

#year
years = []

#grant code
grantCodes = []

#the name of person, used by project_count_search
personName = []

#the institute of person, used by project_count_search
personInstitute = []

#the use of sys.setdefaultencoding() has always been discouraged, and it has become a no-op in py3k. The encoding of py3k is hard-wired to "utf-8" and changing it raises an error.
#if sys.getdefaultencoding() != 'utf-8':
#    reload(sys)
#    sys.setdefaultencoding('utf-8')

def get_logger():
    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create file handler and set level to debug
    fh = TimedRotatingFileHandler('./log/query.log',when="d",interval=1,backupCount=0,encoding='utf-8',delay=0)
    #fh = logging.FileHandler('query.log',mode='a',encoding='utf-8',delay=0)
    fh.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]:%(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

logger = get_logger()
ofile = open('result.txt', "a+")

def save_index(index):
    with open(donefile,'r+') as f:
        f.seek(0)
        f.truncate()
        nu = str(index)
        f.write(nu)

def read_index():
    with open(donefile,'r+') as fi:
        fi.seek(0)
        savedindex = fi.read()
        logger.info ('saved index is:'+savedindex)
        return int(savedindex)

def get_captcha(browser):
    #pdb.set_trace()
    imgelement = browser.find_elements_by_xpath('.//span[@class="number"]/img')[0]
    imgelement.screenshot('captcha.png')
    image = Image.open('captcha.png')
    text = pytesseract.image_to_string(image)
    #logger.info ("captcha:"+text)
    return text

def get_next_page(browser,result_index):  
    try:
        result_id = browser.find_element_by_id(str(result_index))
    except:
        result_id = None
    if (result_id != None):
        return
    while(result_id == None):
        #pdb.set_trace()
        checkcode_in_result = get_captcha(browser)
        if (checkcode_in_result == ""):
            browser.find_element_by_id("img_checkcode").click()
            checkcode_in_result = get_captcha(browser)
        js2 = '$("#checkCode").val("' + checkcode_in_result +'");'
        browser.execute_script(js2)
        browser.find_element_by_id("next_t_TopBarMnt").click()
        result_table = browser.find_element_by_id("dataGrid")
        table_trs = result_table.find_elements_by_tag_name("tr")
        table_tds = table_trs[1].find_elements_by_tag_name("td")
        #the following if-else code exists bugs which may result in infinite loops. I will check later.
        if ( table_tds[0].text == str(result_index)):
            result_id = table_tds[0].text
        else: 
            result_id = None

def submit_form(browser, subjectCode_Id, keyWord, grantCode, year, title):

    js = '$("#f_ctitle").val("' + title +'");'
    # js += '$("#f_subjectCode").val("' + subjectCode +'");'
    # js += '$("#f_subjectCode_hideName").val("' + subjectName +'");'
    js += '$("#f_subjectCode_hideId").val("' + subjectCode_Id +'");'
    js += '$("#sqdm").val("' + subjectCode_Id + '");'
    js += '$("#f_grantCode").val("' + grantCode +'");'
    js += '$("#f_keyWords").val("' + keyWord +'");'
    js += '$("#f_year").val("' + year +'");'

    result_element = None 
    while(result_element == None):
        checkcode = get_captcha(browser)
        if (checkcode == ""):
            browser.find_element_by_id("img_checkcode").click()
            continue
        js1 = '$("#f_checkcode").val("' + checkcode +'");'
        browser.execute_script(js)
        browser.execute_script(js1)
        browser.find_element_by_id("searchBt").click()    
        try:
            result_element = browser.find_element_by_id('sp_2_TopBarMnt')
        except:
            result_element = None

    result_number = result_element.text
    if result_number == '0':
        return
    count = int(result_number)
    logger.debug ('query: subject:%s,keyword:%s,grant:%s,year:%s,title:%s,共%s条结果:',subjectCode_Id,keyWord,grantCode,year,title,result_number)
    ofile.write("query: subject:" + subjectCode_Id + ',keyword:' + keyWord +',grant:' + grantCode + ',year:' + year + ',title:' +title+",共"+result_number+"条结果：\n")
    i = 1
    while( count > 0 ):  
        #pdb.set_trace()    
        get_next_page(browser,i)
        result_table = browser.find_element_by_id("dataGrid")
        table_trs = result_table.find_elements_by_tag_name("tr")
        for tr in table_trs:
            table_tds = tr.find_elements_by_tag_name("td")
            row = ""
            for td in table_tds:
               row += td.text + ','
            row += grantCode + ',' + subjectCode_Id + ',' + keyWord + ',' + year
            logger.debug ('result: %s',row)
            ofile.write("result: " + row +"\n")
        ofile.flush()
        count -= 10
        i += 10

def restart_browser(browser):
    logger.info ("restarting firefox...")
    browser.close()
    bs = webdriver.Firefox()
    bs.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')
    logger.info ("restart done")
    return bs

def project_count_search():
    logger.info ('opening a browser...\n')
    alreadydone = read_index()
    browser = webdriver.Firefox()
    browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')
    for s in open(personnamefile):
        personName.append(s[:-1])
    for s in open(personinstitutefile):
        personInstitute.append(s[:-1])
    
    logger.info ('Name=%s,Institute=%s',personName, personInstitute)
    i = 0
    for personid in personName:
        if alreadydone > i:
            i += 1
            continue
        browser.find_element_by_link_text('人员获资助项目信息查询').click()
        browser.find_element_by_id("resetBt2").click()
        #Python 2 had two global functions to coerce objects into strings: unicode() to coerce them into Unicode strings, and str() to coerce them into non-Unicode strings. Python 3 has only one string type, Unicode strings, so the str() function is all you need. (The unicode() function no longer exists.)
        name = str(personName[i], errors='replace')
        inis = str(personInstitute[i],errors='replace')
        browser.find_element_by_name('psnName_1').send_keys(name)
        browser.find_element_by_name('org_1').send_keys(inis)
        logger.info ('%s,%s,%s',i,personid,personInstitute[i])
        browser.find_element_by_id("searchBt2").click()
        result_table = browser.find_element_by_id("grid_2")
        table_trs = result_table.find_elements_by_tag_name("tr")
        for tr in table_trs:
            table_tds = tr.find_elements_by_tag_name("td")
            row = ""
            for td in table_tds:  
                row += td.text + ','
            ofile.write("result: " + str(i) + ',' + row +"\n")
            logger.debug ('result: %s,%s',i,row)
        ofile.flush()
        i += 1
        save_index(i)
        if (i % 1000 == 0):
            browser = restart_browser(browser)

def auto_search():
    logger.info('opening a browser...')
    alreadydone = read_index()
    #browser = webdriver.Chrome()
    browser = webdriver.Firefox()
    browser.get('https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list')
    index = 0
    for s in open(subjectfile):
        subjectCodeIds.append(s[:-1])
    for s in open(yearfile):
        years.append(s[:-1])
    for s in open(keywordfile):
        allKeyWords.append(s[:-1])
    for s in open(grantfile):
        grantCodes.append(s[:-1])
    logger.info ('allKeyWords=%s,years=%s,subjectCodeIds=%s,grantCodes=%s',allKeyWords,years,subjectCodeIds,grantCodes)
    for subid in subjectCodeIds:
        for grantcode in grantCodes:
            for year in years:
                if len(allKeyWords) > 0:
                    title=''
                    for keyword in allKeyWords:
                        if alreadydone > index:
                            index += 1
                            continue
                        try:
                            submit_form(browser, subid, keyword, grantcode, year, title)
                        except:
                            time.sleep(3)
                        index += 1
                        save_index(int(index))    
                        logger.info ('%s,%s,%s,%s,%s',index,subid,keyword,grantcode,year)
                        if index % 1000  == 0:
                             browser = restart_browser(browser)  
                             continue  
                        try:
                            browser.back()
                        except:
                            logger.error("Timeout loading page. try again...")
                            browser = restart_browser(browser)
                        time.sleep(0.1)
                else :
                    keyword = ''
                    title = ''
                    if alreadydone > index:
                    	index += 1
                    	continue
                    try:
                        submit_form(browser, subid, keyword, grantcode, year, title)
                    except:
                        time.sleep(3)
                    index += 1
                    save_index(index)
                    logger.info ('%s,%s,%s,%s,%s',index,subid,keyword,grantcode,year)
                    if index % 1000  == 0:
                        browser = restart_browser(browser)  
                        continue  
                    try:
                        browser.back()
                    except:
                        logger.error("Timeout loading page. try again...")
                        browser = restart_browser(browser)
                    time.sleep(0.1)

if __name__ == '__main__':
    arg = docopt(__doc__, version='NSFC AutoQuery 0.1')
    if (arg.get('-g') == True or arg.get('--gerernalquery') == True):
        logger.info('GerneralQuery is executed...')
        auto_search()
        logger.info("reset index...and exit. Please find the result.txt for the query. Enjoy.")
    elif (arg.get('-p') == True or arg.get('--projectcount') == True):
        logger.info('ProjectCountQuery is executed...')
        project_count_search()
        logger.info("reset index...and exit. Please find the countofprojects.txt for the query. Enjoy.")
    else:
        logger.info('GerneralQuery is executed...')
        auto_search()
        logger.info("reset index...and exit. Please find the result.txt for the query. Enjoy.")
    
    save_index(0)

    
    