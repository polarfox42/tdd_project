from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows],
                    f'Новый элемент списка не появился в таблице. Содержимым было:\n{table.text}')
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''можно начать список и получить его позже'''
        # Лиса хочет опробовать крутое приложение для составления списка дел
        self.browser.get(self.live_server_url)

        # Заголовок и шапка страницы говорят о списках неотложных дел.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу предлагается ввести элемент списка
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Она набирает в текстовом поле "Купить павлиньи перья"
        inputbox.send_keys('Купить павлиньи перья')

        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать блесну из павлиньих перьев"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать блесну из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)

        # Страница снова обновляется, и теперь показывает оба элемента списка
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать блесну из павлиньих перьев')

        # Лиса видит, что сайт сгенерировал для нее уникальный урл-адрес - об этом
        # выводится небольшой текст с объяснениями
        self.fail('Закончить тест!')

        # Она посещает этот адрес и убеждается, что ее список по-прежнему там.

        # Лиса закрывает браузер и возвращается к своим делам.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Лиса начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Она замечает, что ее список имеет уникальный адрес
        lisa_list_url = self.browser.current_url
        self.assertRegex(lisa_list_url, '/lists/.+')

        # Теперь новый пользователь, Ник, приходит на сайт
        ## Новый сеанс браузера, чтобы никакая инфа не просочилась
        ## через куки
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Ник посещает домашнюю страницу. Нет никаких признаков списка Лисы
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать блесну', page_text)

        # Ник начинает новый список, вводя новый элемент
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Ник получает уникальный адрес списка
        nick_list_url = self.browser.current_url
        self.assertRegex(nick_list_url, '/lists/.+')
        self.assertNotEqual(nick_list_url, lisa_list_url)

        # Ни следа списка Лисы
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

        # Довольные, оба покидают сайт.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
