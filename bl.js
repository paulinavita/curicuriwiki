const puppeteer = require('puppeteer')
const fs = require('fs');

const results = [];
(async () => {
  const browser = await puppeteer.launch({
      headless: false
  })
  const page = await browser.newPage()
  const response = await page.goto("https://api.bukalapak.com/multistrategy-products?prambanan_override=true&keywords=airpods&limit=50&offset=0&page=1&facet=true&access_token=TQMJyTwadbaE98be03GcvtB6a97WWUgGzjmqzmAVslBbDQ", {
      waitUntil: 'networkidle2'
  });
  const jsonRes = await response.json()
  try {
    fs.writeFileSync('airpods.json', JSON.stringify(jsonRes))
  } catch (err) {
    console.error(err)
  }

  await browser.close()
})()