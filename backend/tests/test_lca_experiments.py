from playwright.sync_api import Page, expect


def test_lca_experiments(page: Page) -> None:
    page.goto("http://localhost/")

    # login
    page.get_by_role("link", name="Log In").click()
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill("kkoffi@uidaho.edu")
    page.get_by_label("Email:").press("Tab")
    page.get_by_label("Password:").fill("uidaho")
    page.get_by_role("button", name="Login").click()

    # LCA experiments
    page.get_by_role("link", name="LCA").click()
    page.get_by_role(
        "heading",
        name="Welcome to LCA page, fill out the following information to start an experiment.",
    ).click()
    page.get_by_role("heading", name="Getting started:").click()

    expect(
        page.get_by_text("Manuals, case studies, and databases are available here.")
    ).to_be_visible()

    page.get_by_placeholder("Name of the project").click()
    page.get_by_placeholder("Name of the project").fill("Test")
    page.get_by_placeholder("Name of the project").press("Tab")
    page.locator("#phase1Text").fill("Testing\n          ")
    page.locator("#phase1Text").press("Tab")
    page.get_by_label("Social", exact=True).press("Enter")
    page.get_by_label("Social", exact=True).check()
    page.get_by_label("Social", exact=True).press("Tab")
    page.get_by_label("Importing a database").check()
    page.locator("#txtFileUpload_1").click()

    # file upload
    page.locator("#txtFileUpload_1").set_input_files(
        "./sampleCSVs/SLCA_Education_Example.csv"
    )
    page.get_by_role("button", name="Add new process").click()
    page.get_by_role("button", name="Add new process").click()
    page.get_by_label(
        "Social analysis method:  \n            Indicator Value = Sum m-n [Sum i-n (Score/Total Score)] x Score / Number of Metrics  (see the example on social assessment page)"
    ).check()
    page.locator("#method4").check()

    # pdf generation
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Generate").click()
    download = download_info.value

    # results
    page.locator("#Result2").get_by_text("106.88").click()
    page.locator("#Result1").get_by_text("106.88").click()
