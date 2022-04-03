def get_pagination_range(paginator_dict):
    pag = paginator_dict['paginator']
    start = max(1, paginator_dict['page'] - 3)
    return range(start, min(pag.num_pages+1, start + 5))
