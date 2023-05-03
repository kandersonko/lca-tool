import re
from playwright.sync_api import Page, expect


def test_homepage(page: Page) -> None:
    page.goto("http://localhost/")
    expect(page).to_have_title(re.compile("CyberTraining @ Uni. of Idaho"))

    expect(page.get_by_role("link", name="Home")).to_be_visible()
    expect(page.get_by_role("link", name="Register")).to_be_visible()
    expect(page.get_by_role("link", name="Log In")).to_be_visible()
    expect(page.get_by_role("link", name="University of Idaho")).to_be_visible()
    expect(page.get_by_role("link", name="CyberTraining")).to_be_visible()
    expect(
        page.get_by_role(
            "link",
            name="Research and Innovation in Sustainable Manufacturing and Materials",
        )
    ).to_be_visible()

    page.get_by_role("link", name="Register").click()
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("link", name="Home").click()
