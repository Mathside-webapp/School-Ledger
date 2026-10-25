"""Add offline CanteenLedger icons to freshly generated Capacitor Android resources."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent.parent
RES=ROOT/'android'/'app'/'src'/'main'/'res'
ASSET=ROOT/'resources'
assert RES.exists(), 'Generate the Android project with npx cap add android first.'
for folder,size in [('mipmap-mdpi',48),('mipmap-hdpi',72),('mipmap-xhdpi',96),('mipmap-xxhdpi',144),('mipmap-xxxhdpi',192)]:
    destination=RES/folder
    destination.mkdir(parents=True,exist_ok=True)
    filename=ASSET/f'icon-{size}.png'
    assert filename.exists(), f'Missing {filename}'
    shutil.copy2(filename,destination/'ic_launcher.png')
    shutil.copy2(filename,destination/'ic_launcher_round.png')
# Supply splash image via drawable, using a subtle cream backdrop.
drawable=RES/'drawable';drawable.mkdir(exist_ok=True,parents=True)
shutil.copy2(ASSET/'splash.png',drawable/'splash.png')
print('Installed Android launcher icons and splash asset.')
