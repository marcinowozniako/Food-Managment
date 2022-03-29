from django.core.paginator import Paginator


class PaginatorClass:
    def __init__(self, request, to_paginate, records_on_page):
        self.request = request
        self.to_paginate = to_paginate
        self.records_on_page = records_on_page

    def prepare_paginator(self):
        pag = Paginator(self.to_paginate, self.records_on_page)
        page_request = self.request.GET.get('page')
        page = 1
        if page_request is not None:
            page = int(self.request.GET.get('page'))

        on_page = pag.get_page(page)
        return {'paginator': pag, 'page': page, 'on_page': on_page}