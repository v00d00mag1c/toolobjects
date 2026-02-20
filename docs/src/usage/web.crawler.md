### Web page downloading

create new:

```
python tool.py -i Web.Pages.Crawler.Webdrivers.Chromedriver.Create -executable_path {path to browser} -set_as_current 1
```

get it id and set it in the `web.crawler.webdriver` field.

to download a page:

```
python tool.py -i Web.Pages.Get -url {{url}}
```
