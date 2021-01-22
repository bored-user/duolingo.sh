# duolingo.sh

Python script to extend Duolingo to the terminal!<br>
It uses [`pyppeteer`](https://github.com/pyppeteer/pyppeteer) (unnoficial port of Javascript's `puppeteer`) as a headless browser and extract informations directly from Duolingo's website.

### Usage

When executing the script for the first time, one'll be asked to input their Duolingo's email adress/ username and password. This will be stored in a `config.json` file on the script's root, as follows:
```json
{
    "auth": {
        "email": "example@domain.com",
        "password": "MySuperSecurePassword"
    }
}
```

After the first execution, however, the script will automatically detect the configuration file and read info from it.<br>
Note that the user will also be asked to input an integer indicating the lesson to be exercised. After that, all that's left to do is reading and answering the questions (will appear on terminal as well).

### Dependencies

The only 3rd party module imported by `duolingo.sh` is, as previuosly said, `pyppeteer`.

### BTW

You, my fellow programmer and Duolingo user, may be interested in [`streakpy`](https://github.com/bored-user/streakpy). A bot to keep Duolingo streaks going (also writen in Python). Check it out!

As always, feel free to open issues and PRs. All help is welcome.
Happy coding!
