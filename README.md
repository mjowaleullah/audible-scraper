
# audible-scraper
A robust Python web scraper built with Selenium to extract audiobook listings from Audible. Features automated pagination via URL query parameters, anti-bot/Cloudflare bypass, and CSV data export.

# 📚 Audible Audiobooks Scraper

A robust Python web scraper built using **Selenium WebDriver** to extract audiobook listings from Audible.com. It is designed to handle JavaScript-rendered dynamic content, bypass anti-bot mechanisms, navigate multi-page pagination, and export clean structured data into CSV format.

## 🌟 Features

- **Anti-Bot Bypass:** Uses specialized Chrome options and custom User-Agent headers to prevent Cloudflare/WAF detection.
- **Dynamic Content Extraction:** Waits for AJAX elements using Selenium `WebDriverWait`.
- **Reliable Pagination:** Loops through catalog pages seamlessly via URL Query Parameters (`?page=N`).
- **Automatic Driver Management:** Integrates `webdriver-manager` to avoid ChromeDriver version mismatch errors.
- **Structured Export:** Cleans raw extracted strings and exports to CSV.

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Automation Framework:** Selenium WebDriver
- **Utilities:** WebDriver Manager, CSV

## 📊 Extracted Data Schema

The scraper extracts the following fields for each audiobook:

| Field | Description | Example |
| :--- | :--- | :--- |
| `page` | Catalog page number | `1` |
| `title` | Audiobook Title | *Delving and Dating* |
| `author` | Author(s) Name | *Daniel Schinhofen* |
| `length` | Audio Runtime | *9 hrs and 21 mins* |
| `ratings` | Rating Score | *4.8* |

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone [https://github.com/mowaleullah/audible-scraper.git](https://github.com/mjowaleullah/audible-scraper.git)
cd audible-scraper

