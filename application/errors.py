from flask import render_template

from application.meta_tags_dict import metaTags as meta


class ErrorsHandle(object):
    """
    Class to serve errors pages
    """

    def __init__(self, arg):
        super(ErrorsHandle, self).__init__()
        self.arg = arg

    def page_not_found(self, e):
        return render_template('error_pages/404.html',
                               titleText=meta["error404"]["pageTitleDict"],
                               headerText=meta["error404"]["headerDict"]), 404

    def request_entity_too_large(self, e):
        return render_template('error_pages/413.html',
                               titleText=meta["error413"]["pageTitleDict"],
                               headerText=meta["error413"]["headerDict"]), 413
