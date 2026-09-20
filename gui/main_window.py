import customtkinter as ctk


class MainWindow:
    def __init__(self, root, config, controller, state):
        self.root = root
        self.config = config
        self.controller = controller
        self.state = state

        self.main = ctk.CTkFrame(root, corner_radius=14)
        self.main.pack(fill='both', expand=True, padx=16, pady=16)
        ctk.CTkLabel(self.main, text='WEB AUTOMATION BOT', font=('Segoe UI', 26, 'bold')).pack(pady=(12, 10))

        form = ctk.CTkFrame(self.main, fg_color='transparent')
        form.pack(fill='x', padx=16, pady=8)
        ctk.CTkLabel(form, text='Website URL:').pack(anchor='w')
        self.url_entry = ctk.CTkEntry(form, width=700, placeholder_text='https://example.com')
        self.url_entry.pack(fill='x', pady=(4, 10))
        self.url_entry.insert(0, self.config.get('url', 'https://example.com'))

        browser_row = ctk.CTkFrame(form, fg_color='transparent')
        browser_row.pack(fill='x')
        ctk.CTkButton(browser_row, text='OPEN BROWSER', command=self.open_browser).pack(side='left', padx=(0, 10))
        ctk.CTkButton(browser_row, text='SAVE CONFIG', command=self.save_config).pack(side='left', padx=(0, 10))
        ctk.CTkButton(browser_row, text='RESET CONFIG', command=self.reset_config).pack(side='left')

        target_frame = ctk.CTkFrame(form, fg_color='transparent')
        target_frame.pack(fill='x', pady=(12, 8))
        self.selector_type = ctk.CTkOptionMenu(target_frame, values=['css', 'xpath', 'text', 'role', 'aria'])
        self.selector_type.pack(side='left', padx=(0, 10))
        self.selector_type.set(self.config.get('selector_type', 'css'))
        self.selector_entry = ctk.CTkEntry(target_frame, placeholder_text='Selector / Text / Role', width=520)
        self.selector_entry.pack(side='left', fill='x', expand=True)
        self.selector_entry.insert(0, self.config.get('selector', '#submit-button'))

        action_row = ctk.CTkFrame(form, fg_color='transparent')
        action_row.pack(fill='x', pady=(8, 10))
        ctk.CTkButton(action_row, text='PICK ELEMENT', command=self.pick_element).pack(side='left', padx=(0, 10))
        ctk.CTkButton(action_row, text='TEST CLICK', command=self.test_click).pack(side='left')

        mode_frame = ctk.CTkFrame(form, fg_color='transparent')
        mode_frame.pack(fill='x', pady=(6, 0))
        self.mode_var = ctk.StringVar(value=self.config.get('mode', 'manual'))
        self.mode_option = ctk.CTkOptionMenu(
            mode_frame, variable=self.mode_var,
            values=['manual', 'scheduled', 'detection', 'hybrid'],
        )
        self.mode_option.pack(side='left', padx=(0, 12))
        ctk.CTkLabel(mode_frame, text='Mode (manual = refresh + notification, no automatic click)').pack(side='left')

        schedule_frame = ctk.CTkFrame(form, fg_color='transparent')
        schedule_frame.pack(fill='x', pady=(12, 0))
        ctk.CTkLabel(schedule_frame, text='Start Time').pack(side='left', padx=(0, 8))
        self.start_time = ctk.CTkEntry(schedule_frame, width=120)
        self.start_time.pack(side='left', padx=(0, 12))
        self.start_time.insert(0, self.config.get('schedule', {}).get('start_time', 'now'))

        ctk.CTkLabel(schedule_frame, text='Refresh (sec)').pack(side='left', padx=(0, 8))
        self.refresh_interval = ctk.CTkEntry(schedule_frame, width=90)
        self.refresh_interval.pack(side='left', padx=(0, 12))
        self.refresh_interval.insert(0, str(self.config.get('refresh', {}).get('interval_seconds', 10)))

        ctk.CTkLabel(schedule_frame, text='Click Count').pack(side='left', padx=(0, 8))
        self.click_count = ctk.CTkEntry(schedule_frame, width=90)
        self.click_count.pack(side='left')
        self.click_count.insert(0, str(self.config.get('schedule', {}).get('click_count', 1)))

        detection_frame = ctk.CTkFrame(form, fg_color='transparent')
        detection_frame.pack(fill='x', pady=(12, 0))
        ctk.CTkLabel(detection_frame, text='Detection Type').pack(side='left', padx=(0, 8))
        self.detection_type = ctk.CTkOptionMenu(
            detection_frame,
            values=['element_appears', 'element_becomes_visible', 'element_becomes_enabled', 'text_appears', 'text_changes', 'url_changes'],
        )
        self.detection_type.pack(side='left', padx=(0, 12))
        self.detection_type.set(self.config.get('detection', {}).get('type', 'element_becomes_enabled'))

        ctk.CTkLabel(detection_frame, text='Detection selector').pack(side='left', padx=(0, 8))
        self.detection_selector = ctk.CTkEntry(detection_frame, width=200)
        self.detection_selector.pack(side='left', padx=(0, 12))
        self.detection_selector.insert(0, self.config.get('detection', {}).get('selector', 'button'))

        ctk.CTkLabel(detection_frame, text='Expected text').pack(side='left', padx=(0, 8))
        self.expected_text = ctk.CTkEntry(detection_frame, width=150)
        self.expected_text.pack(side='left')
        self.expected_text.insert(0, self.config.get('detection', {}).get('expected_text', 'Buy Ticket'))

        controls = ctk.CTkFrame(form, fg_color='transparent')
        controls.pack(fill='x', pady=(18, 8))
        ctk.CTkButton(controls, text='START', command=self.start).pack(side='left', padx=(0, 10))
        ctk.CTkButton(controls, text='PAUSE', command=self.pause).pack(side='left', padx=(0, 10))
        ctk.CTkButton(controls, text='RESUME', command=self.resume).pack(side='left', padx=(0, 10))
        ctk.CTkButton(controls, text='STOP', command=self.stop).pack(side='left')

        self.status_var = ctk.StringVar(value='● IDLE')
        ctk.CTkLabel(form, textvariable=self.status_var, font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(10, 6))
        self.log_box = ctk.CTkTextbox(self.main, height=12, wrap='word')
        self.log_box.pack(fill='both', padx=16, pady=(0, 16), expand=True)
        self.log_box.insert('end', '[INFO] Web Automation Bot started\n')
        self.log_box.configure(state='disabled')

    def open_browser(self):
        self.config.set('url', self.url_entry.get().strip())
        self.config.save()
        self.controller.start()
        self.status_var.set('● RUNNING')

    def pick_element(self):
        self.status_var.set('● PICKING')
        self._log('[INFO] Element picker enabled. Click an element in the browser.')

    def test_click(self):
        self.config.set('selector', self.selector_entry.get().strip())
        self.config.set('selector_type', self.selector_type.get())
        self.config.save()
        self.controller.test_click()

    def save_config(self):
        self.config.set('url', self.url_entry.get().strip())
        self.config.set('selector', self.selector_entry.get().strip())
        self.config.set('selector_type', self.selector_type.get())
        self.config.set('mode', self.mode_var.get())
        schedule = self.config.get('schedule', {})
        schedule['start_time'] = self.start_time.get().strip()
        schedule['click_count'] = int(self.click_count.get().strip())
        self.config.set('schedule', schedule)
        refresh = self.config.get('refresh', {})
        refresh['interval_seconds'] = max(5.0, float(self.refresh_interval.get().strip()))
        refresh['notify_only'] = True
        self.config.set('refresh', refresh)
        detection = self.config.get('detection', {})
        detection['type'] = self.detection_type.get()
        detection['selector'] = self.detection_selector.get().strip()
        detection['expected_text'] = self.expected_text.get().strip()
        self.config.set('detection', detection)
        self.config.save()
        self._log('[INFO] Configuration saved. Manual mode never clicks automatically.')

    def reset_config(self):
        self.config.reset()
        self.url_entry.delete(0, 'end')
        self.url_entry.insert(0, self.config.get('url', 'https://example.com'))
        self.selector_entry.delete(0, 'end')
        self.selector_entry.insert(0, self.config.get('selector', '#submit-button'))
        self.selector_type.set(self.config.get('selector_type', 'css'))
        self.status_var.set('● IDLE')

    def start(self):
        self.save_config()
        self.controller.start()
        self.status_var.set('● RUNNING')

    def pause(self):
        self.controller.pause()
        self.status_var.set('● PAUSED')

    def resume(self):
        self.controller.resume()
        self.status_var.set('● RUNNING')

    def stop(self):
        self.controller.stop()
        self.status_var.set('● STOPPED')

    def _log(self, message):
        self.log_box.configure(state='normal')
        self.log_box.insert('end', message + '\n')
        self.log_box.see('end')
        self.log_box.configure(state='disabled')

    def handle_event(self, event):
        if not event:
            return
        level, message = event
        self._log(f'[{level}] {message}')
        self.status_var.set(f'● {self.controller.state.value}')
