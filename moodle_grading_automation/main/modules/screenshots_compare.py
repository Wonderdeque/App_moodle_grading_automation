from cgitb import html, text
from re import I
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
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

img_a = Image.open("page.png")
widthA, heightA = img_a.size
print(img_a.size)

with sync_playwright() as p:
    browser = p.webkit.launch()
    context = browser.new_context(viewport={ 'width': widthA, 'height': heightA })
    page = context.new_page()
    page.goto("https://danila-fedortsov.github.io/public/index.html")
    page.screenshot(path="screenshots/screenshot.png")
    browser.close()


img_b = Image.open("screenshots/screenshot.png")
print(img_b.size)
img_diff = Image.new("RGBA", img_a.size)

# note how there is no need to specify dimensions
mismatch = pixelmatch(img_a, img_b, img_diff, includeAA=True,threshold = 0.4)
img_diff.save("diff.png")
percentage_of_diff = mismatch / (widthA * heightA)
print("diff = {:.2f}%".format(percentage_of_diff))
