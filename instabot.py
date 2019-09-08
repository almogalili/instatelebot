from selenium import webdriver
import time


class InstagramBot:

    def __init__(self):
        self.images = []
        self.username = 'username'  # here you have to pass usernmae and password for login
        self.password = 'pass'
        self.base_url = 'https://www.instagram.com'
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.posts_urls = []
        self.login()

    def login(self):
        login_page = '{}/accounts/login/'.format(self.base_url)
        username_xpath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input'
        password_xpath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input'
        logging_button_xpath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div'

        self.driver.get(login_page)
        time.sleep(1)

        self.driver.find_element_by_xpath(username_xpath).send_keys(self.username)
        time.sleep(1)

        self.driver.find_element_by_xpath(password_xpath).send_keys(self.password)
        time.sleep(1)

        self.driver.find_element_by_xpath(logging_button_xpath).click()
        time.sleep(3)

    def nav_user(self, user):
        self.driver.get('{}/{}'.format(self.base_url, user))

    # we need to scroll down and to save the posts urls into an array, i did it in this way for maybe in the future to dowload also videos.
    def scroll_down(self):

        posts_xpath = "//*[@class='v1Nh3 kIKUG  _bz0w']//a"
        last_height = self.driver.execute_script('return document.body.scrollHeight')
        time.sleep(3)

        while True:
            # now we have to store the posts urls.
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            path = self.driver.find_elements_by_xpath(posts_xpath)
            time.sleep(1)
            self.add_posts_urls(path)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # this condition checking if we have to scroll down more.
            if last_height == new_height:
                return

            last_height = new_height

    def add_posts_urls(self, path):

        for i in path:
            url = i.get_attribute('href')
            if url not in self.posts_urls:
                self.posts_urls.append(url)

    def get_images_from_posts(self):

        for url in self.posts_urls:
            self.driver.execute_script("window.open('" + url + "', '_self')")
            self.driver.implicitly_wait(2)
            imagesXpath = self.driver.find_elements_by_xpath("//*[@class='FFVAD']")

            for x in imagesXpath:
                img = x.get_attribute("srcset")
                # in srcset there's about 3-4 resolution images url seperated by ,
                img = img.split(",")
                img = img[-1][:-6]
                print(img)
                if img not in self.images and img is not None:
                    # last one being highest res image -4 to escape resolution X*X in url
                    self.images.append(img)

    def get_images(self, username):
        self.nav_user(username)
        self.scroll_down()
        self.get_images_from_posts()

        return self.images
