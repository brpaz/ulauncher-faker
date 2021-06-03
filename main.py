""" Main Module """

import logging
from faker import Faker
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)

FAKER_PROVIDERS = sorted([
    'address', 'building_number', 'city', 'city_suffix', 'country',
    'country_code', 'postcode', 'street_address', 'street_name',
    'street_suffix', 'license_plate', 'iban', 'bban', 'swift11', 'swift8',
    'hex_color', 'rgb_color', 'bs', 'catch_phrase', 'company',
    'company_suffix', 'credit_card_full', 'credit_card_number',
    'credit_card_provider', 'credit_card_security_code', 'pricetag', 'date',
    'date_this_month', 'date_this_decade', 'date_this_year'
    'date_of_birth', 'date_time_this_decade', 'date_time_this_month',
    'date_time_this_year', 'day_of_month', 'day_of_week', 'future_date',
    'future_datetime', 'iso8601', 'month', 'month_name', 'past_date',
    'past_datetime', 'time', 'unix_time', 'year', 'coordinate', 'latitude',
    'latlng', 'longitude', 'file_path', 'mime_type', 'unix_device',
    'unix_partition', 'ascii_company_email', 'ascii_email', 'ascii_free_email',
    'ascii_safe_email', 'company_email', 'domain_name', 'domain_word', 'email',
    'free_email', 'free_email_domain', 'hostname', 'image_url', 'ipv4',
    'ipv4_private', 'ipv4_public', 'ipv6', 'mac_address', 'port_number',
    'slug', 'uri', 'user_name', 'isbn10', 'isbn13', 'job', 'paragraph',
    'sentence', 'text', 'word', 'binary', 'md5', 'password', 'sha1', 'sha256',
    'uuid4', 'first_name', 'first_name_male', 'last_name', 'last_name_male',
    'last_name_female', 'name', 'name_female', 'name_male',
    'country_calling_code', 'phone_number', 'msisdn', 'ssn',
    'android_platform_token', 'chrome', 'firefox', 'ios_platform_token',
    'linux_platform_token', 'linux_processor', 'mac_platform_token',
    'user_agent', 'windows_platform_token'
])


class FakerExtension(Extension):
    """ Main Extension Class  """
    def __init__(self):
        """ Initializes the extension """
        super(FakerExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.fake = Faker()

    def list_providers(self, query):

        providers = FAKER_PROVIDERS
        if query:
            providers = [
                provider for provider in providers if query.lower() in provider
            ]

        items = []

        if len(providers) == 0:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name="No provider found matching your criteria",
                    highlightable=False,
                    on_enter=HideWindowAction())
            ])

        for provider in providers[:20]:
            items.append(
                ExtensionSmallResultItem(
                    icon='images/icon.png',
                    name=provider.replace("_", " ").title(),
                    on_enter=ExtensionCustomAction(provider,
                                                   keep_app_open=True)))

        return RenderResultListAction(items)


class KeywordQueryEventListener(EventListener):
    """ Listener that handles the user input """
    def on_event(self, event, extension):
        """ Handles the event """
        return extension.list_providers(event.get_argument())


class ItemEnterEventListener(EventListener):
    """ Listener that handles the click on an item """
    def on_event(self, event, extension):
        """ Handles the event """
        selected_provider = event.get_data()
        Faker.seed(0)

        items = []

        for _ in range(10):
            val = getattr(extension.fake, selected_provider)()
            items.append(
                ExtensionSmallResultItem(icon='images/icon.png',
                                         name=val,
                                         highlightable=False,
                                         on_enter=CopyToClipboardAction(val)))

        return RenderResultListAction(items)


if __name__ == '__main__':
    FakerExtension().run()
