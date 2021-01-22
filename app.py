import asyncio
import json
import os

import login
import lesson


async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    config = {
        'auth': {}
    }

    browser, page = await login.get_credentials(config) if not login.check_credentials(config) else await login.login(config['auth']['email'], config['auth']['password'])
    print('Logged in!')

    await lesson.wait_loading('div[data-test=skill-icon]', page)
    print('Finding available lessons (this can take a while)')
    available_lessons = await lesson.find_available_lessons(page)
    skill = lesson.get_lesson(available_lessons)
    await lesson.start(skill, page)
    await lesson.loop(page)

    await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
