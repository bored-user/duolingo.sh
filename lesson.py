import os
import re
import time


async def wait_loading(query, page, once=False):
    element = await page.querySelector(query)

    while element == None and not once:
        await page.screenshot({'path': 'realtime.png'})
        element = await page.querySelector(query)
        time.sleep(0.1)

    await page.screenshot({'path': 'realtime.png'})
    return element


async def find_available_lessons(page):
    skills = await page.querySelectorAll('div[data-test=skill]')
    titles = []

    for i in range(len(skills)):
        titles.append((await page.evaluate('s => s.textContent', skills[i])))
        await skills[i].click()

        if await page.evaluate("p => p.textContent.toUpperCase().includes('LOCKED')", await wait_loading('div[data-test=skill-popout]', page)):
            return [titles[j] for j in range(i - 1)]


def get_lesson(skills) -> int:
    width = len(str(len(skills) + 1))

    for i in range(len(skills)):
        print(f"[{str(i + 1).rjust(width, '0')}]. {skills[i][1:] if re.search('[0-9]', skills[i][0]) != None else skills[i]}")

    try:
        return int(input('> Input the lesson to practice: '))
    except ValueError:
        print(f'Please, enter a number from 1 to {len(skills)}')
        time.sleep(3)
        return get_lesson(skills)


async def start(skill: int, page):
    await (await page.querySelectorAll('div[data-test=skill]'))[skill - 1].click()
    await wait_loading('div[data-test=skill-popout]', page)
    await (await page.querySelector('button[data-test=start-button]')).click()
    await wait_loading('button[data-test=quit-button]', page)


async def loop(page):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        header = await page.querySelectorEval('[data-test=challenge-header]', 'h => h.textContent')
        keyboard = await page.querySelector('button[data-test=player-toggle-keyboard]')
        is_keyboard_on = await page.evaluate("k => !k.textContent.toUpperCase().includes('KEYBOARD')", keyboard) if not keyboard == None else False

        if not await page.querySelector('div[data-test=challenge-translate-prompt]') == None:
            print(await get_words(page))
            answer = input(f'> {header}: ')

            if not keyboard == None:
                if not is_keyboard_on:
                    await keyboard.click()

                textarea = await wait_loading('textarea[data-test=challenge-translate-input]', page)
                await textarea.type(answer)
                await (await page.querySelector('button[data-test=player-next]')).click()
        elif not await page.querySelector('div[data-test=challenge-form-prompt]') == None:
            pass

async def get_words(page): return (await page.querySelectorAllEval('span[data-test=hint-sentence] > *', "words => words.map(word => word.innerHTML).join('')"))
