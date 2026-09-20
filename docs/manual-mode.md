# Manual refresh mode

The recommended mode for sites that restrict automation is `manual`.

In manual mode the app:

1. Opens the configured page.
2. Waits until `schedule.start_time` (`now` or `HH:MM:SS`).
3. Refreshes at a conservative interval. Values below 5 seconds are clamped to 5 seconds.
4. Checks whether the configured target is visible and enabled.
5. Logs `TARGET READY` and emits a Windows notification sound.
6. Never clicks automatically; the user clicks in the visible browser.

Example:

```json
{
  "mode": "manual",
  "selector_type": "text",
  "selector": "Buy Ticket",
  "schedule": { "start_time": "10:00:00" },
  "refresh": { "interval_seconds": 10, "notify_only": true }
}
```

Use only on websites that permit this assistance. Do not use the application to bypass CAPTCHA, queues, access controls, or other anti-bot protections.
