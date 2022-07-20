import scrapy
import json

class ProductSpider(scrapy.Spider):
    name = 'Product'
    allowed_domains = ['www.zoro.com']
    start_urls = ['http://www.zoro.com/']

    def parse(self, response):
        data = response.css('script').re('window.INITIAL_STATE = "{(.*)}"')[0]
        data = '{' + data + '}'
        data = data.replace('\\\"', '"')
        data = data.replace('\\x3C', '<')
        data = data.replace('\\\\n', '')
        data = data.replace('\\\\\"', '\\\"')
        data = data.replace('\\x26', '')
        data = json.loads(data)
        data = data['category']
        for main_cat in data['navigationCategories']:
            for sub_cat in main_cat['children']:
                yield scrapy.Request(response.urljoin(sub_cat['slug']+'/c/'+sub_cat['code']+'/'), self.parse_cat)
    
    def parse_cat(self, response):
       yield from response.follow_all(css='ul.c-sidebar-nav__list li.c-sidebar-nav__list-child a', callback=self.parse_sub_cat)
    
    def parse_sub_cat(self, response):
        product_links = response.css('section.search-results div.product-card a.title::attr(href)')
        for link in product_links[0:10]:
            yield response.follow(link, callback=self.parse_product)
    
    def parse_product(self, response):
        name = response.css('h1[data-za=product-name]::text').get().strip()
        zoro = response.css('span[data-za="PDPZoroNo"]::text').get().strip()
        mfr = response.css('span[data-za="PDPMfrNo"]::text').get().strip()
        brand = response.css('a[data-za="product-brand-name"]::text').get().strip()
        category = ' / '.join(response.css('ol.Breadcrumb li.Breadcrumb__list-item a.Breadcrumb__link span::text').getall()[1:-1])
        price = response.css('span.product-price__price::attr(content)').get()
        description = response.css('div.description-container div::text').get().strip()
        yield {
            'title': name,
            'zoro_id': zoro,
            'mfr_no': mfr,
            'brand': brand,
            'price': price,
            'category': category,
            'description': description
        }
       


                
           