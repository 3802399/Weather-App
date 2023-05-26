import settings
import gui
import weather

class Main:
    def __init__(self):
        preferred_display = settings.Settings.get_display_mode()

        if preferred_display == "gui":
            self.open_gui()
        elif preferred_display == "cli":
            self.open_cli()
        else:
            print("Error: display mode in settings must either be 'gui' or 'cli'. ")
            restoration = input("Would you like to restore it via this app? (y/n)")

            if restoration.lower() == "y":
                display = ""

                while display != "gui" and display != "cli":
                    display = input("Enter display mode ('gui' or 'cli'): ").lower()

                settings.Settings.
