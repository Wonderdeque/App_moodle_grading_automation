from cgitb import html, text
from re import I
from django.conf import settings
from playwright.sync_api import sync_playwright
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch



# with sync_playwright() as p:
#     p.devices
#     iphone_11 = p.devices['iPhone 11 Pro']
#     browser = p.webkit.launch(headless=False)
#     context = browser.new_context(
#         **iphone_11,
#         locale='de-DE',
#         geolocation={ 'longitude': 12.492507, 'latitude': 41.889938 },
#         permissions=['geolocation']
#     )
#     page = context.new_page()
#     page.goto("https://danila-fedortsov.github.io/public/index.html")
#     browser.close()
def get_match_points_and_diff_screen(url):
    img_a = Image.open("static/compare_screenshots/etalon_screens/page.png")
    widthA, heightA = img_a.size
    print(img_a.size)

    with sync_playwright() as p:
        browser = p.webkit.launch()
        context = browser.new_context(viewport={ 'width': widthA, 'height': heightA })
        page = context.new_page()
        page.goto(url)
        page.screenshot(path="static/compare_screenshots/stud_screens/screenshot.png")
        browser.close()


    img_b = Image.open("static/compare_screenshots/stud_screens/screenshot.png")
    print(img_b.size)
    img_diff = Image.new("RGBA", img_a.size)

    # note how there is no need to specify dimensions
    mismatch = pixelmatch(img_a, img_b, img_diff, includeAA=True,threshold = 0.4)
    img_diff.save("static/compare_screenshots/diff_screens/diff.png")
    percentage_of_diff = mismatch / (widthA * heightA)
    print("diff = {:.2f}%".format(percentage_of_diff))

    return img_a,img_b,img_diff,percentage_of_diff
