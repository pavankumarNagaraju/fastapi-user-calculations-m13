import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"


@pytest.mark.e2e
def test_register_positive(page: Page):
    page.goto(f"{BASE_URL}/static/register.html")

    page.get_by_test_id("register-email").fill("e2euser@example.com")
    page.get_by_test_id("register-fullname").fill("E2E User")
    page.get_by_test_id("register-password").fill("secret123")
    page.get_by_test_id("register-confirm-password").fill("secret123")

    page.get_by_test_id("register-submit").click()

    message = page.locator("#message")
    expect(message).to_contain_text("Registration successful")


@pytest.mark.e2e
def test_register_short_password_negative(page: Page):
    page.goto(f"{BASE_URL}/static/register.html")

    page.get_by_test_id("register-email").fill("shortpass@example.com")
    page.get_by_test_id("register-fullname").fill("Short Pass")
    page.get_by_test_id("register-password").fill("123")
    page.get_by_test_id("register-confirm-password").fill("123")

    page.get_by_test_id("register-submit").click()

    message = page.locator("#message")
    expect(message).to_contain_text("Password must be at least 6 characters.")


@pytest.mark.e2e
def test_login_positive(page: Page):
    page.goto(f"{BASE_URL}/static/login.html")

    page.get_by_test_id("login-email").fill("e2euser@example.com")
    page.get_by_test_id("login-password").fill("secret123")

    page.get_by_test_id("login-submit").click()

    message = page.locator("#message")
    expect(message).to_contain_text("Login successful")


@pytest.mark.e2e
def test_login_wrong_password_negative(page: Page):
    page.goto(f"{BASE_URL}/static/login.html")

    page.get_by_test_id("login-email").fill("e2euser@example.com")
    page.get_by_test_id("login-password").fill("wrong-pass")

    page.get_by_test_id("login-submit").click()

    message = page.locator("#message")
    expect(message).to_contain_text("Invalid credentials")
