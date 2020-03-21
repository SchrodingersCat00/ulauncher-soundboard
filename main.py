import os

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction


EXTENSION_ICON = 'images/icon.png'
HOME = os.getenv("HOME")
sound_files = [sound_file.name[:-4] for sound_file in os.scandir('%s/.local/share/ulauncher/extensions/soundboard/sound_files/' % HOME)]


class ItemEnterEventListener(EventListener):

    def play_sound(self, sound_name):
        os.system("mpg123 ~/.local/share/ulauncher/extensions/soundboard/sound_files/\"" + sound_name + ".mp3\"")

    def on_event(self, event, extension):
        data = event.get_data()
        self.play_sound(data)


class SoundboardExtension(Extension):

    def __init__(self):
        super(SoundboardExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        # placeholder item
        if not event.get_argument():
            return RenderResultListAction([
                ExtensionResultItem(icon=EXTENSION_ICON,
                                    name='Type in sound name...',
                                    on_enter=DoNothingAction())
            ])
        # if a query is given
        items = []
        for name in sound_files:
            if event.get_argument().lower() in name.lower():
                items.append(ExtensionResultItem(
                    icon=EXTENSION_ICON,
                    name=name,
                    description='Play %s' % name,
                    on_enter=ExtensionCustomAction(name, keep_app_open=False)))

        return RenderResultListAction(items)

if __name__ == '__main__':
    SoundboardExtension().run()
