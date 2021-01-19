import json
import os
import time

import pyppeteer

import lesson


def check_credentials(config):
    if os.path.isfile('config.json'):
        config['auth'] = json.load(open('config.json', 'r'))['auth']
        return True

    return False


async def get_credentials(config):
    print('Please, input your')

    email = input('     > Duolingo\'s account email address (or username): ')
    password = input('      > Duolingo\'s account password: ')

    browser, page = await login(email, password, config)

    config['auth']['email'] = email
    config['auth']['password'] = password
    json.dump(config, open('config.json', 'w'))

    return browser, page


async def login(email, password, config=None):
    browser = await pyppeteer.launch()
    page = await browser.newPage()

    await page.setViewport({'width': 1920, 'height': 948})
    await page.goto('https://www.duolingo.com/')

    await (await lesson.wait_loading('a[data-test=have-account]', page)).click()
    await (await page.querySelector("input[placeholder='Email or username']")).type(email)
    await (await page.querySelector("input[placeholder='Password']")).type(password)
    await (await page.querySelector('button[type=submit]')).click()

    error = await lesson.wait_loading('div[data-test=invalid-form-field]', page, True)
    return browser, page if error == None else handle_login_errors(error, config)


async def handle_login_errors(error, config):
    print(error)
    time.sleep(3)
    return await get_credentials(config)
