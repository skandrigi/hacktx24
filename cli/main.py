from textual.app import App


class ScreenApp(App):
    def on_mount(self) -> None:
        self.screen.styles.background = "#161b2a"
        self.screen.styles.border = ("heavy", "white")


if __name__ == "__main__":
    app = ScreenApp()
    app.run()