class _AddFlowerPage:

    INDEX_PAGE = '/init_flower_post.html'

    def __init__(self, database, render_template):
        self.engine = database
        self.render_template = render_template

    @property
    def html(self):
        return self.generate_page()


    def generate_page(self):
        return self.render_template(self.INDEX_PAGE)

    @classmethod
    def show(cls, database, render_template):
        page = cls(database, render_template)
        return page.html


class AddFlowerPage:
    def __new__(cls, db, render_template):
        return _AddFlowerPage.show(db, render_template)
