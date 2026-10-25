"""Install CanteenLedger legacy + adaptive icons on freshly generated Capacitor Android.

This is purposely self-contained: it only uses Python's standard library so it works
in GitHub Actions without pip-installing Pillow or any other imaging package.
"""
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
RES=ROOT/'android'/'app'/'src'/'main'/'res'
ASSETS=ROOT/'resources'
MANIFEST=ROOT/'android'/'app'/'src'/'main'/'AndroidManifest.xml'
ANDROID_NS='http://schemas.android.com/apk/res/android'
assert RES.exists(), 'Android platform not found. Run npx cap add android and npx cap sync android first.'

# Android 7 and earlier (legacy raster launcher assets). Remove generated .webp
# files, since two resources with the same name but different extensions conflict.
for folder,size in [('mipmap-mdpi',48),('mipmap-hdpi',72),('mipmap-xhdpi',96),
                    ('mipmap-xxhdpi',144),('mipmap-xxxhdpi',192)]:
    dest=RES/folder;dest.mkdir(parents=True,exist_ok=True)
    icon=ASSETS/f'icon-{size}.png'
    assert icon.is_file(),f'Missing CanteenLedger resource: {icon}'
    for name in ('ic_launcher','ic_launcher_round'):
        for old in dest.glob(f'{name}.*'):
            old.unlink()
        shutil.copy2(icon,dest/f'{name}.png')

# Android 8+ uses *adaptive* icons from mipmap-anydpi-v26. Capacitor's defaults
# remain visible if only the legacy files above are changed.
img=RES/'drawable-nodpi';img.mkdir(parents=True,exist_ok=True)
for src,name in [('android-adaptive-foreground.png','canteen_launcher_foreground.png'),
                 ('android-adaptive-monochrome.png','canteen_launcher_monochrome.png')]:
    source=ASSETS/src
    assert source.is_file(), f'Missing adaptive icon layer: {source}'
    shutil.copy2(source,img/name)

# Add a dedicated brand color, without overwriting existing Android colors.
values=RES/'values';values.mkdir(parents=True,exist_ok=True)
(values/'canteen_launcher_background.xml').write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<resources><color name="canteen_launcher_background">#174B3B</color></resources>\n',
    encoding='utf-8')
adaptive=RES/'mipmap-anydpi-v26';adaptive.mkdir(parents=True,exist_ok=True)
xml=('<?xml version="1.0" encoding="utf-8"?>\n'
     '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
     '  <background android:drawable="@color/canteen_launcher_background" />\n'
     '  <foreground android:drawable="@drawable/canteen_launcher_foreground" />\n'
     '  <monochrome android:drawable="@drawable/canteen_launcher_monochrome" />\n'
     '</adaptive-icon>\n')
for name in ('ic_launcher.xml','ic_launcher_round.xml'):
    (adaptive/name).write_text(xml,encoding='utf-8')

# Ensure generated AndroidManifest points at our launcher icons.
assert MANIFEST.exists(), f'Missing Android manifest: {MANIFEST}'
ET.register_namespace('android',ANDROID_NS)
manifest=ET.parse(MANIFEST);app=manifest.getroot().find('application')
assert app is not None, 'AndroidManifest has no <application> element.'
app.set(f'{{{ANDROID_NS}}}icon','@mipmap/ic_launcher')
app.set(f'{{{ANDROID_NS}}}roundIcon','@mipmap/ic_launcher_round')
manifest.write(MANIFEST,encoding='utf-8',xml_declaration=True)

# Preserve the original standalone offline splash, and keep brand-specific image.
drawable=RES/'drawable';drawable.mkdir(exist_ok=True,parents=True)
shutil.copy2(ASSETS/'splash.png',drawable/'splash.png')

# Fail the CI job if a generated Capacitor adaptive icon was left behind.
for name in ('ic_launcher.xml','ic_launcher_round.xml'):
    actual=(adaptive/name).read_text(encoding='utf-8')
    assert '@drawable/canteen_launcher_foreground' in actual
assert (img/'canteen_launcher_foreground.png').stat().st_size>100
assert app.attrib.get(f'{{{ANDROID_NS}}}icon')=='@mipmap/ic_launcher'
print('CanteenLedger icon fix applied: 5 legacy densities, adaptive/round/themed icon, Android manifest, splash.')
