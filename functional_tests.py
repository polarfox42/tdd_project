from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''можно начать список и получить его позже'''
        # Лиса хочет опробовать крутое приложение для составления списка дел
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1. Купить павлиньи перья' for row in rows)
        )

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать блесну из павлиньих перьев"
        self.fail('Закончить тест!')

        # Страница снова обновляется, и теперь показывает оба элемента списка

        # Лиса видит, что сайт сгенерировал для нее уникальный урл-адрес - об этом
        # выводится небольшой текст с объяснениями

        # Она посещает этот адрес и убеждается, что ее список по-прежнему там.

        # Лиса закрывает браузер и возвращается к своим делам.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
