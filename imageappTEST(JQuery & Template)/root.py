import quixote
from quixote.directory import Directory, export, subdir

from . import html, image, javascript, css

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data)

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        response.set_content_type('image/png')
        img = image.get_latest_image()
        return img

    @export(name='jquery.js')
    def jquery(self):
        return javascript.render("jquery-1.11.0.min.js")

    @export(name='ajax_upload_image.js')
    def ajax_upload(self):
        return javascript.render("ajax_upload_image.js")

    @export(name='style.css')
    def style_css_upload(self):
        return css.render("style.css")