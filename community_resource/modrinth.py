import modrinth_api_wrapper, os, re
import modrinth_api_wrapper.models
import requests as web

class SearchReturningPage():
    def __init__(self, page_size = 10, page_number_index = 0) -> None:
        self.page_size = page_size
        self.page_index = page_number_index
        self.page_range = (page_number_index * page_size, (page_number_index + 1) * page_size - 1)

def search_project(query: str = None, page = SearchReturningPage()) -> modrinth_api_wrapper.models.SearchResult:
    client = modrinth_api_wrapper.Client()
    search_response: modrinth_api_wrapper.models.SearchResult = client.search_project(query=query, limit=page.page_size, offset=page.page_range[0])
    os.makedirs("community_cache/modrinth/icons", exist_ok=True)
    for resource in search_response.hits:
        if not os.path.isfile("community_cache/modrinth/icons/{0}{1}".format(resource.project_id, re.findall(r"\.\w+$", resource.icon_url)[0])):
            resource_icon = web.get(resource.icon_url).content
            with open("community_cache/modrinth/icons/{0}{1}".format(resource.project_id, re.findall(r"\.\w+$", resource.icon_url)[0]), mode="wb") as icon_file:
                icon_file.write(resource_icon)
    return search_response

SearchResultType = modrinth_api_wrapper.models.SearchResult