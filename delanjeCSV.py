import orodja
import re

##Pripravi CSV za depository
def priprava_depository():
	regex_knjige = re.compile(
		r'<meta itemprop="author" content="(?P<avtor>.*?)".*?'
                r'<h1 itemprop="name">(?P<naslov>.*?)<.*?'
                r'<div class="item-info-wrap">\s*<p class="price">\s*(?P<cenaE>\d*,\d{2}).*?'
                r'<label>Format</label>\s*<span>\s*(?P<format>\w*).*?'
                r'"numberOfPages">(\d+).*?"datePublished">(?P<datum>\d{2} \w{3} \d{4}).*?'
                r'Language</label>\s*<span>\s*(?P<jezik>\w*).*?'
                r'ISBN10</label>\s*<span>(?P<ISBN10>\d{10}).*?'
                r'ISBN13</label>\s*<span itemprop="isbn">(?P<ISBN13>\d{13})',
		flags=re.S
	)

	knjige = {}
	for html_datoteka in orodja.datoteke('podatki/depositoryISBN/'):
		for knjiga in re.finditer(regex_knjige, orodja.vsebina_datoteke(html_datoteka)):
			podatki=knjiga.groupdict()
			knjige[podatki['ISBN10']]=podatki
	orodja.zapisi_tabelo(sorted(knjige.values(), key=lambda knjiga: knjiga['ISBN10']),
                             ['ISBN10','avtor', 'naslov', 'cenaE', 'format','jezik','datum','ISBN13'],
                             'csv-datoteke/depository2.csv')


#Pripravi CSV iz Amazona
def priprava_amazon():
	regex_knjige = re.compile(
		r'gp/product-reviews/(?P<ISBN10>\d{10}).{150,200}?\$\d*\.\d{2} \$(?P<cenaD>\d*\.\d{2})',
		flags=re.S
	)

	knjige = {}
	for html_datoteka in orodja.datoteke('podatki/amazon5/'):
		for knjiga in re.finditer(regex_knjige, orodja.vsebina_datoteke(html_datoteka)):
			podatki=knjiga.groupdict()
			knjige[podatki['ISBN10']]=podatki
	orodja.zapisi_tabelo(sorted(knjige.values(), key=lambda knjiga: knjiga['ISBN10']),
                             ['ISBN10','cenaD'], 'csv-datoteke/amazon2.csv')


#Naredi seznam ISBN-jev zajetih s Parse 
def zajemi_isbn():
	regex_isbn=re.compile(
		r'gp/product-reviews/(\d{10}).{150,200}?\$\d*\.\d{2} \$(\d*\.\d{2})',
		flags=re.S
	)

	seznamISBN=[]

	for html_datoteka in orodja.datoteke('podatki/amazon/'):
		for knjiga in re.finditer(regex_isbn, orodja.vsebina_datoteke(html_datoteka)):
			seznamISBN.append(knjiga.group(1))

	return seznamISBN

#S seznamom (isbnjev pridobljenih iz amazona ali parsa) pobere strani z Depositorya
for isbn10 in seznamISBN:
        url='https://www.bookdepository.com/search?searchTerm=&searchTitle=&searchAuthor=&searchPublisher=&searchIsbn={}&searchLang=&advanced=true'.format(isbn10)
        mesto='podatki/DepositoryISBN/{}'.format(isbn10)
        shrani(url,mesto)
		
