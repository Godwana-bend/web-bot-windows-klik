# Web Automation Bot

A modern Windows desktop application for browser automation using Python, Playwright Chromium, and CustomTkinter.

## Features

- Persistent Chromium profile in `profiles/default` so users can log in once and reuse the session
- DOM-based target selection with CSS, XPath, text, role, and aria selector support
- Target picker to click an element and auto-generate a selector
- Scheduled click automation with start time, interval, maximum click count, and repeat options
- MutationObserver-driven detection for element appears, visible/enabled changes, text changes, URL changes, and attribute changes
- Hybrid mode that triggers only within an active time window
- Cooldown and rate limiting to avoid spam clicks
- Start, pause, resume, stop, and test-click controls
- JSON configuration, logging to `logs/bot.log`, and a Windows-friendly PyInstaller build

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Running

```bash
python main.py
```

## Browser Profile

The app uses a persistent browser context under:

```text
profiles/default/
```

This keeps cookies, login sessions, and local storage between runs. Users must log in manually when needed.

## Element Picker

From the main window, click `PICK ELEMENT`, then click any visible element in the browser. The app records element metadata and attempts to generate the best selector automatically. It is then editable in the selector field before execution.

## Scheduled Click

Use the `Start Time`, `Interval`, and `Click Count` fields to queue repeated actions. The app waits asynchronously instead of blocking the GUI thread with `time.sleep()`.

## Page Change Detection

The detection engine uses `MutationObserver` in the page context to watch DOM mutations without reloading the page repeatedly. This keeps CPU usage low and makes triggers more responsive.

## Hybrid Mode

Hybrid mode combines scheduled triggers and DOM detection, enabling automation only within the active time range.

## Configuration

Configurations are stored in `config.json` and can be saved or reset from the UI. The app also supports a default template in `config/default_config.json`.

## Troubleshooting

- If Chromium is missing, run `playwright install chromium`.
- If selectors fail, open DevTools and verify the target element structure.
- If the browser profile becomes stale, remove the `profiles/default` folder and re-login.
- Review `logs/bot.log` for any errors.

## Build Windows EXE

```bat
build.bat
```

The output is generated into the `dist` folder as a PyInstaller executable.

## Security

Use this tool only on websites and systems you are authorized to access and operate within the site policy. Do not use the bot for CAPTCHA bypass, login bypass, anti-bot evasion, or any access-control bypass. Passwords are never stored in the source code.

## Limitations

- Websites can change their DOM structure or require more resilient selectors.
- Some dynamic websites may need custom selectors or event timing adjustments.
- This is a desktop automation utility, not a browser-automation bypass tool.

## Example Use

1. Open the app.
2. Enter `https://example.com`.
3. Set the selector type to `css`.
4. Set the selector to `#submit-button`.
5. Click `START`.
6. Use `TEST CLICK` to validate the target before starting the full automation.
