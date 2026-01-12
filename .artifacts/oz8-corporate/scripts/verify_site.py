#!/usr/bin/env python3
"""OZ8 Corporate Website Verification Script

Tests both Japanese and English versions of the site:
- Homepage
- About page
- Achievements page
- Contact page
- Language switching
"""

from playwright.sync_api import sync_playwright
import time
import os

BASE_URL = os.environ.get('BASE_URL', 'http://localhost:4321')
ARTIFACTS_DIR = '.artifacts/oz8-corporate/images'

def capture_screenshot(page, filename, full_page=True):
    """Capture screenshot with timestamp"""
    timestamp = int(time.time())
    path = f"{ARTIFACTS_DIR}/{timestamp}-{filename}"
    page.screenshot(path=path, full_page=full_page)
    print(f"✓ Saved: {path}")
    return path

def test_site():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1440, 'height': 900},
            locale='ja-JP'
        )
        page = context.new_page()

        # Collect console logs and errors
        console_logs = []
        page.on('console', lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))

        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))

        failed_requests = []
        page.on('requestfailed', lambda req: failed_requests.append(req.url))

        print("\n=== Testing Japanese Version ===\n")

        # 1. Homepage (Japanese)
        print("1. Testing Homepage (Japanese)...")
        page.goto(BASE_URL, wait_until='networkidle')
        page.wait_for_timeout(1000)
        capture_screenshot(page, 'ja-01-homepage.png')

        # Check key elements
        assert page.locator('h1:has-text("OZ8株式会社")').is_visible(), "Company name not found"
        assert page.locator('text=トラベル＆リラックスグッズ').first.is_visible(), "Subtitle not found"
        print("   ✓ Key elements visible")

        # 2. About page (Japanese)
        print("\n2. Testing About page (Japanese)...")
        page.click('text=会社概要')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        capture_screenshot(page, 'ja-02-about.png')
        assert page.locator('text=岡崎よしあき').is_visible(), "Representative name not found"
        print("   ✓ About page loaded")

        # 3. Achievements page (Japanese)
        print("\n3. Testing Achievements page (Japanese)...")
        page.click('text=実績')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        capture_screenshot(page, 'ja-03-achievements.png')
        assert page.locator('text=Makuake').first.is_visible(), "Makuake achievement not found"
        print("   ✓ Achievements page loaded")

        # 4. Contact page (Japanese)
        print("\n4. Testing Contact page (Japanese)...")
        page.click('text=お問い合わせ')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        capture_screenshot(page, 'ja-04-contact.png')
        assert page.locator('text=ozeight@gmail.com').first.is_visible(), "Email not found"
        print("   ✓ Contact page loaded")

        print("\n=== Testing English Version ===\n")

        # 5. Switch to English
        print("5. Switching to English...")
        page.click('text=English')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        capture_screenshot(page, 'en-01-contact.png')
        assert page.locator('text=Contact Us').is_visible(), "English content not found"
        print("   ✓ Language switched to English")

        # 6. Homepage (English)
        print("\n6. Testing Homepage (English)...")
        page.click('text=Home')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        capture_screenshot(page, 'en-02-homepage.png')
        assert page.locator('h1:has-text("OZ8 Corporation")').is_visible(), "Company name (EN) not found"
        print("   ✓ English homepage loaded")

        # 7. About page (English)
        print("\n7. Testing About page (English)...")
        page.click('text=About')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        capture_screenshot(page, 'en-03-about.png')
        assert page.locator('text=Yoshiaki Okazaki').is_visible(), "Representative name (EN) not found"
        print("   ✓ English about page loaded")

        # 8. Achievements page (English)
        print("\n8. Testing Achievements page (English)...")
        page.click('text=Achievements')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        capture_screenshot(page, 'en-04-achievements.png')
        assert page.locator('text=Makuake').first.is_visible(), "Makuake achievement (EN) not found"
        print("   ✓ English achievements page loaded")

        # 9. Mobile viewport test (Japanese homepage)
        print("\n9. Testing Mobile viewport...")
        page.set_viewport_size({'width': 375, 'height': 667})
        page.goto(BASE_URL, wait_until='networkidle')
        page.wait_for_timeout(1000)
        capture_screenshot(page, 'mobile-01-homepage.png')
        print("   ✓ Mobile viewport tested")

        # 10. Tablet viewport test
        print("\n10. Testing Tablet viewport...")
        page.set_viewport_size({'width': 768, 'height': 1024})
        page.goto(BASE_URL, wait_until='networkidle')
        page.wait_for_timeout(1000)
        capture_screenshot(page, 'tablet-01-homepage.png')
        print("   ✓ Tablet viewport tested")

        browser.close()

        # Report results
        print("\n" + "="*50)
        print("VERIFICATION RESULTS")
        print("="*50)
        print(f"✓ All tests passed")
        print(f"✓ Screenshots saved: {ARTIFACTS_DIR}")

        if console_logs:
            print(f"\n⚠ Console logs: {len(console_logs)}")
            for log in console_logs[:5]:  # Show first 5
                print(f"  {log}")

        if errors:
            print(f"\n❌ Page errors: {len(errors)}")
            for error in errors:
                print(f"  {error}")

        if failed_requests:
            print(f"\n❌ Failed requests: {len(failed_requests)}")
            for url in failed_requests[:5]:  # Show first 5
                print(f"  {url}")

        if not errors and not failed_requests:
            print("\n✓ No errors detected")

if __name__ == '__main__':
    test_site()
