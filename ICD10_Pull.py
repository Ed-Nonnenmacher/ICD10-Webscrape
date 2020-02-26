import re,sys,bs4,requests,time
import pandas as pd

reg=re.compile(r'.+?(?=[A-Z]{1}[1-9]{1,3}\.[A-Z1-9]{1,2})|(?=[A-Z]{1}[1-9]{1,3}\.[A-Z1-9]{1,2}).+?$')
reg1=re.compile(r'.+?\w\d{1,2}\.[A-Z1-9]{1,4}|\w\d{1,2}\.[A-Z1-9]{1,4}.+?$')
reg2=re.compile(r'\w\d{1,3}\.[A-Z0-9]{1,4}.+?(?=\w\d{1,3}\.[A-Z0-9]{1,4})|(?=\w\d{1,3}\.[A-Z0-9]{1,4}).+?$')

class icd_scrape:
    def __init__(self,base_url=r'https://www.icd10data.com/ICD10CM/Codes/'):
        self.base_url=base_url
        self.wp=requests.get(base_url)
        self.page=bs4.BeautifulSoup(self.wp.text,features='html.parser')
        self.icd_reg=re.compile(r'.+?(?=[A-Z]\d{2}\.\d{1,4})|(?=[A-Z]\d{2}\.\d{1,4}).+?$|(?=[A-Z]\d{2}).+|.+?(?=\w{3,4}\.)|(?=\w{3,4}\.).+?$')

    def icd_ranger_base(self):
        base_reg=re.compile(r'<a class="identifier" href="\/ICD10CM\/Codes\/\w\d{2}-\w[\w\d]{2}">(.*?)<\/a>')
        body=self.page('div',{'class':'body-content'})#this is the body of html that holds all li tags of interest
        return [base_reg.search(str(i)).group(1) for i in body[0]('a',{'class':'identifier'})]  #body stores result into a single item list, which much be indexed, and then can be iterated over

    def icd_ranger_L1(self):
        content=self.page('ul',{'class':'i51'})[0]
        return [i.text[:7] for i in content.select('li')]

    def icd_ranger_L2(self):
        content=self.page('ul',{'class':'i51'})[0]
        return [i.text[1:4]+'-' for i in content.select('li')]

    def is_4th(self,i0,i1,i2):
        self.fourth_level=[]
        self.codes=[]
        for i in icds.icd_reg.findall(icds.page.select_one('ul[class^=codeHierarchy]').text):
            try:
                i.split(' ')[0][-1]=='-'
            except IndexError:
                continue
            if i.split(' ')[0][-1]=='-':
                print('4th level: '+i.split(' ')[0])
                self.fourth_level.append(icds.base_url+i0+'\\'+i1+'\\'+i2[:3]+'\\'+i.split(' ')[0])
            else:
                self.codes.append([i.split(' ')[1].split(' ')[0] if i.split(' ')[0]=='' else i.split(' ')[0],' '.join(i.split(' ')[1:])])
    def icd_extractor(self,i0,i1,i2):
        self.is_4th(i0,i1,i2)

        for i in self.fourth_level:
            wp=requests.get(i)
            page=bs4.BeautifulSoup(wp.text)
            text=page.select('ul[class=codeHierarchy]',features='html.parser')[-1].text
            self.codes.extend([[i.split(' ')[1].split(' ')[0] if i.split(' ')[0]=='' else i.split(' ')[0],' '.join(i.split(' ')[1:])] for i in self.icd_reg.findall(text)])
            time.sleep(1.5)

        #text=self.page.select_one('li[class^=codeLine]').text
        #self.codes.extend([[i.split(' ')[1].split(' ')[0] if i.split(' ')[0]=='' else i.split(' ')[0],' '.join(i.split(' ')[1:])] for i in self.icd_reg.findall(text)])
        return self.codes     
    def up_1_level(self,ext):
        self.wp=requests.get(self.base_url+ext)
        self.page=bs4.BeautifulSoup(self.wp.text,features='html.parser')



if '__main__'==__name__:
    scraped_icd=[]
    icds=icd_scrape()
    icd_range0=icds.icd_ranger_base()#instancing class along and calling for base ranges of al ICD's
    for i0 in icd_range0:
        icds.up_1_level(i0)
        icd_range1=icds.icd_ranger_L1()
        for i1 in icd_range1:
            icds.up_1_level(f'{i0}\\{i1}')
            icd_range2=icds.icd_ranger_L2()
            for i2 in icd_range2:
                icds.up_1_level(f'{i0}\\{i1}\\{i2}')
                print(icds.wp.url)
                
                if icds.icd_extractor(i0,i1,i2)==[]:
                    scraped_icd.append(icds.wp.url) 
                for i in icds.icd_extractor(i0,i1,i2):
                    print(i)
                    scraped_icd.append(i)
                    
                time.sleep(1.5)
    df=pd.DataFrame(scraped_icd)
    df.to_csv('icd_beta_otp.csv')
    






##Scrap Code


'''for i in a[68211:]:
	if '……' in i[1]:
		if 'X' in i[0].split('.')[1]:
			d.append([i[0],b.get('.'.join([i[0].split('.')[0],i[0].split('.')[1].split('X')[0]]))+i[1][3:]])
			continue
		d.append([i[0],b.get(i[0][:len(i[0])-1])+i[1][3:]])
		continue
	else:
		d.append(i)'''

'''for i in a[68211:]
	if '……' in i[1]:
		if 'X' in i[0].split('.')[1]:
			d.append([i[0],b.get('.'.join([i[0].split('.')[0],i[0].split('.')[1].split('X')[0]]))+i[1][3:]])
			continue
		d.append([i[0],b.get(i[0][:len(i[0])-1])+i[1][3:]])
		continue
	else:
		d.append(i)'''


