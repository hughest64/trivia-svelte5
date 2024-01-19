from django.conf import settings

import qrcode
import qrcode.image.svg

# for now the only option is to return an svg string, but this could be expanded a greate deal:
# - png option
# - show option
# - store in db option(s)
# - etc, etc, etc

SITE_LINK = settings.EMAIL_REDIRECT_HOST

class TeamQr:
    def __init__(self, team_password) -> None:
        self.team_password = team_password
        self.img = None
        self.svg_string = None

    def create(self):
        qr = qrcode.QRCode(
            box_size=15,
            image_factory=qrcode.image.svg.SvgPathImage,

        )
        qr.add_data(self._make_url())

        self.img = qr.make_image()
        self.svg_string = self.img.to_string(encoding='unicode')

        return self.svg_string
    
    def _make_url(self):
        return f"{SITE_LINK}/team/join?password={self.team_password}"