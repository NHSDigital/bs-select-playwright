import random
import string
import pytest
from pages.rlp_location_list_page import ScreeningLocationListPage
from playwright.sync_api import expect, Page
from datetime import datetime


def generate_random_string(length=random.randint(3, 100)):
    characters = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join(random.choices(characters, k=length))
