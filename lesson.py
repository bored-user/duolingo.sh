import os
import re
import time
import urllib.parse

from colorama import Fore, Style


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
            return [titles[j] for j in range(i)]


def get_lesson(skills) -> int:
    [print(f"[{str(i + 1).rjust(len(str(len(skills) + 1)), '0')}]. {skills[i][1:] if re.search('[0-9]', skills[i][0]) != None else skills[i]}") for i in range(len(skills))]

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
    async def enable_keyboard():
        if not is_keyboard_on:
            await keyboard.click()

    async def click_next():
        await wait_loading('body', page, True)
        await (await page.querySelector('button[data-test=player-next]')).click()

    async def check_answer():
        await wait_loading('body', page, True)
        result = await page.querySelector('div[data-test*=blame]')


        print(
            f"{Fore.RED}Incorrect!{Style.RESET_ALL}: {await page.evaluate('d => d.children[1].firstChild.firstChild.children[1].textContent', result)}"
                if await page.evaluate("d => d.getAttribute('data-test').includes('incorrect')", result)
                else
            f'{Fore.GREEN}Correct!{Style.RESET_ALL}'
        )

        time.sleep(3)
        await click_next()

    async def translate_prompt():
        print(await get_words(page, 'span[data-test=hint-sentence] > *'))
        answer = input(f'> Input your answer: ')

        if keyboard:
            await enable_keyboard()

        await (await wait_loading('textarea[data-test=challenge-translate-input]', page)).type(answer)

    async def form_prompt():
        print('form prompt here!')

    async def judge():
        print(await page.evaluate('h => h.parentElement.nextElementSibling.firstChild.textContent', header))

        options = await get_words(page, 'div[data-test=challenge-judge-text]', False)
        [print(f"[{str(i + 1).rjust(len(str(len(options) + 1)), '0')}]. {options[i]}") for i in range(len(options))]

        try:
            answer = int(input('> Input your answer: '))
        except ValueError:
            print(f'Please, enter a number from 1 to {len(options)}')
            time.sleep(3)
            return judge()

        await (await page.querySelectorAll('label[data-test=challenge-choice]'))[answer - 1].click()

    while True:
        do_not_check_answer = False
        os.system('cls' if os.name == 'nt' else 'clear')
        await wait_loading('body', page, True)

        try:
            header = await page.querySelector('h1[data-test=challenge-header]')
            keyboard = await page.querySelector('button[data-test=player-toggle-keyboard]')
            is_keyboard_on = await page.evaluate("k => !k.textContent.toUpperCase().includes('KEYBOARD')", keyboard) if keyboard else True
        except:
            await click_next()

        if await page.querySelector('div[data-test=challenge-translate-prompt]'):
            print(await page.evaluate('h => h.textContent', header))
            await translate_prompt()
        elif await page.querySelector('div[data-test=challenge-form-prompt]'):
            print(await page.evaluate('h => h.textContent', header))
            await form_prompt()
        elif await page.querySelector("div[data-test='challenge challenge-judge']"):
            print(await page.evaluate('h => h.textContent', header))
            await judge()
        elif await page.querySelector("div[data-test='challenge challenge-listenTap']"):
            do_not_check_answer = True
            await (await page.querySelector('button[data-test=player-skip]')).click()
        else:
            print('Oooops, exercise-type handler not programmed yet! Sorry')

            try:
                language_code = re.search(r'\/.*\/(.*)\/.*\/[0-9]*', urllib.parse.urlparse(page.url).path)[1]
                print(f"Create a new issue in https://github.com/bored-user/duolingo.sh/issues/new\nwith the '[{language_code}] missing code for exercise-type' title\n\nPlease, attach the `realtime.png` image to the issue and the exercise header (that should've shown up on your terminal).\nIf possible, also state the exercise type (listening, speaking, type what you hear, etc.).")
            except IndexError:
                print("     Oooops (#2), when trying to identify the language code based on the URL, another exception occured (lmao, shame on me).\n     Please, go to https://github.com/bored-user/duolingo.sh/issues/new and create an issue named 'Error while trying to identify the language code'.\n      Please, also attach the `realtime.png` image file and state the Duolingo URL you were on (not 'duolingo.com/learn'. Should be something like 'duolingo.com/skill/[language_code]/[lesson_name]/[some_number]').")

            exit(1)

        await click_next()
        if not do_not_check_answer:
            await check_answer()

        await wait_loading('body', page, True)
        time.sleep(0.5)


async def get_words(page, query, join=True): return (await page.querySelectorAllEval(query, f"words => words.map(word => word.textContent){'.join(``)' if join else ''}"))
