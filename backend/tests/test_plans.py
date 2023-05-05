from playwright.sync_api import Page, expect


def test_plans(page: Page) -> None:
    page.goto("http://localhost/")

    # login
    page.get_by_role("link", name="Log In").click()
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill("kkoffi@uidaho.edu")
    page.get_by_label("Email:").press("Tab")
    page.get_by_label("Password:").fill("uidaho")
    page.get_by_label("Password:").press("Enter")

    # select plans
    page.get_by_role("link", name="Plans").click()
    page.locator("#plan-select").select_option("premium")
    page.locator("#plan-select").select_option("enterprise")
    page.locator("#plan-select").select_option("premium")

    with page.expect_download() as download_info:
        page.get_by_role("link", name="SampleCSV.csv").click()
    download = download_info.value

    page.locator("#plan-select").select_option("enterprise")
    expect(page.get_by_role("button", name="Choose Plan")).to_be_visible()
    expect(page.get_by_role("heading", name="Choose a Plan")).to_be_visible()
