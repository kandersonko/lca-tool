from playwright.sync_api import Page, expect


def test_login(page: Page) -> None:
    page.goto("http://localhost/")

    page.get_by_role("link", name="Log In").click()
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill("kkoffi@uidaho.edu")
    page.get_by_label("Email:").press("Tab")
    page.get_by_label("Password:").fill("uidaho")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_role("heading", name="Welcome Koffi")).to_be_visible()
    expect(page.get_by_text("Email: kkoffi@uidaho.edu")).to_be_visible()
    expect(page.get_by_text("First name: Koffi Anderson")).to_be_visible()
    expect(page.get_by_text("Last name: Koffi")).to_be_visible()
    expect(page.get_by_text("Affiliation: University of Idaho")).to_be_visible()

    page.get_by_role("link", name="Cycon").click()
    page.get_by_role("link", name="LCA").click()
    page.get_by_role("link", name="Plans").click()
    page.get_by_role("link", name="Home").click()
    page.get_by_role("link", name="Log Out").click()
