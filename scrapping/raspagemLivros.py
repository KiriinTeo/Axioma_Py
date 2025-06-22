import scrapy
from scrapy.crawler import CrawlerProcess

class LivrosSpider(scrapy.Spider):
    name = 'livros'
    start_urls = ['https://www.amazon.com/s?k=gaming&_encoding=UTF8&content-id=amzn1.sym.860dbf94-9f09-4ada-8615-32eb5ada253a&pd_rd_r=b46006ba-f643-44c5-9831-1c0047a54350&pd_rd_w=O9scL&pd_rd_wg=ck4mg&pf_rd_p=860dbf94-9f09-4ada-8615-32eb5ada253a&pf_rd_r=1CYC6394SG1347BXZM34&ref=pd_hp_d_atf_unk']

    def parse(self, response):
        # Extraindo títulos e preços
        for prod in response.css('.product_pod'):
            yield {
                'Título': prod.css('h3 a::attr(title)').get(),
                'Preço': prod.css('.price_color::text').get()
            }
        # Navegar para a próxima página
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)


process = CrawlerProcess()
process.crawl(LivrosSpider)
process.start()
