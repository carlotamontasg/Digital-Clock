import flet as ft
import datetime
import threading

def main(page: ft.Page):
    page.title = "Digital Clock"

    page.fonts = {
        "DigitalFont": "https://github.com/carlotamontasg/Digital-Clock/raw/main/DS-DIGII.TTF"
    }

    current_offset = datetime.timedelta(0)
    timer = None  

    text_style = ft.TextStyle(font_family="DigitalFont", size=150)

    clock_text = ft.Text(
        value=(datetime.datetime.now() + current_offset).strftime("%H:%M:%S"),
        style=text_style,
        text_align=ft.TextAlign.CENTER
    )

    def update_time():
        nonlocal timer, current_offset
        now = datetime.datetime.now() + current_offset
        clock_text.value = now.strftime("%H:%M:%S")
        page.update()

        if timer is not None:
            timer.cancel()

        timer = threading.Timer(1.0, update_time)
        timer.start()

    update_time()

    time_input = ft.TextField(hint_text="Change time (HH:MM:SS)", expand=1)

    def change_time(e):
        nonlocal current_offset
        try:
            new_time = datetime.datetime.strptime(time_input.value, "%H:%M:%S")
            current_time = datetime.datetime.now()
            current_offset = new_time - current_time
            update_time()  
        except ValueError:
            page.snack_bar(ft.SnackBar(content=ft.Text("Invalid time format. Use HH:MM:SS")))

    change_time_button = ft.ElevatedButton(text="Change Time", on_click=change_time)

    page.add(clock_text, time_input, change_time_button)

ft.app(target=main)
