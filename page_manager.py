from math import ceil
from api import DOMAIN_NAME

class PagesManager():
    """Класс позволяющий мониторить данные о странице возврата результата запроса."""

    def __init__(self) -> None:
        pass 

    def generate_json_data(res,route_name,is_generate_data = True) -> dict:

        offset = (res.page-1) * res.per_page
        return {

            "links": {
                "first": f"{DOMAIN_NAME}/{route_name}?page=1",
                "last": f"{DOMAIN_NAME}/{route_name}?page={res.pages}",
                "prev": f"{DOMAIN_NAME}/{route_name}?page={res.prev_num if res.has_prev else res.page}",
                "next": f"{DOMAIN_NAME}/{route_name}?page={res.next_num if res.has_next else res.page}"
            },
            "current_page": res.page,
            "from": offset,
            "last_page": res.pages,
            "path": f"{DOMAIN_NAME}/{route_name}",
            "per_page": res.per_page,
            "to": offset+len(res.items),
            "total": res.total,
            "data": [
                _.json_view() for _ in res.items
            ] if is_generate_data else []
        }

    pass
