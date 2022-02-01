import scrapy


class MidsouthPrimerSpider(scrapy.Spider):
    name = 'midsouth_primer'
    allowed_domains = ['https://www.midsouthshooterssupply.com/']
    start_urls = ['https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1/']

    def parse(self, response):
        print("procesing:"+response.url)
        #Extract data using xpath 
        price=response.xpath("//div[@class='catalog-item-price']/span[@class='price']/span[@class='']/text()").extract()
        #Extract data using css selectors
        title=response.css(".catalog-item-name::text").extract()
        
        stock=response.xpath("//div[@class='catalog-item-price']/div/div/span[@class='status']/span/text()").extract() #instock(true) or out-stock(false)
        maftr= response.css(".catalog-item-brand::text").extract()   #manufacturer

        row_data=zip(price,title,stock,maftr)

        #Making extracted data row wise
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                #key:value
                'page':response.url,
                'price' : float(item[0][1:]),#item[0] means product in the list and so on, index tells what value to assign
                'title' : item[1],
                'stock' : (False) if ('Out' in item[2]) else (True),
                'maftr' : item[3],
            }

            #yield or give the scraped info to scrapy
            yield scraped_info
