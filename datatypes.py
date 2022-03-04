class Item:

    def __init__(self, url, nzb_url, title, description, length, language, posted, file_size,
                 files, group,category, newznab_category1):
        self.url = url
        self.nzb_url = nzb_url
        self.title = title
        self.description = description
        self.length = length
        self.language = language
        self.posted = posted
        self.file_size = file_size
        self.category = category
        self.files = files
        self.group = group
        self.newznab_category1 = newznab_category1