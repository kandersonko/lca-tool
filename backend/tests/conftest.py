import pytest
from playwright.sync_api import Playwright, BrowserContext
from backend import factory


@pytest.fixture()
def app():
    app = factory.create_app(password_file="db/password.txt")
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def browser_context(playwright: Playwright) -> BrowserContext:
    # Create a browser context with ignoreHTTPSErrors set to True
    browser = playwright.chromium.launch()
    context = browser.new_context(ignore_https_errors=True)
    yield context
    context.close()
    browser.close()
