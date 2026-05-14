import { chromium } from "playwright";
import fs from "fs";

type RawDeal = {
  source: string;
  imageUrl: string;
  sourcePage: string;

  title?: string;
  priceText?: string;
  cuisine?: string;

  merchant?: string;
  eligibility?: string[];
  expiresAt?: string;
};

async function scrapeCollinsPromotions() {
  const browser = await chromium.launch({
    headless: true,
  });

  const page = await browser.newPage();

  await page.goto("https://www.collins.sg/promotions", {
    waitUntil: "networkidle",
  });

  const imageUrls = await page.$$eval("img", (images) =>
    images.map((img) => img.src)
  );

  const promoImages = imageUrls.filter((url) =>
    url.includes("squarespace-cdn")
  );

  const deals: RawDeal[] = promoImages.map((url, index) => ({
    source: "Collins",
    imageUrl: url,
    sourcePage: "https://www.collins.sg/promotions",

    // temporary mock enrichment
    title: `Collins Promo ${index + 1}`,
    priceText: "Unknown",
    cuisine: "Western",
    }));

  fs.writeFileSync(
    "./src/scrapers/collins-deals.json",
    JSON.stringify(deals, null, 2)
  );

  console.log(deals);

  await browser.close();
}

scrapeCollinsPromotions();