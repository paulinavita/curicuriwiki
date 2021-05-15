const puppeteer = require('puppeteer');
const $ = require('cheerio');
const fs = require('fs')

let browser = ''
const initScrape = async () => {
  // Initiate browser
  browser = await puppeteer.launch({headless : false});
  const page = await browser.newPage();

  // Navigate to url, wait until page loads
  await page.goto('https://en.wikipedia.org/wiki/List_of_Romantic_composers', {waitUntil : 'domcontentloaded'})
  getList(page)
}

const getList = async (page) => {
  try {
    const recordList = await page.$$eval('#mw-content-text > div.mw-parser-output > table:nth-child(9)',(table)=>{
      let rowList = []
      table.forEach(row => {
        const trList = Array.from(row.querySelectorAll('tr'), column => column.innerText)
        const headerRow = trList[0].split('\t')
        
        trList.forEach((data, i) => {
          let record = headerRow.reduce((o, key) => ({ ...o, [key]: ''}), {})
          if (i > 0) {
            let eachTdInRow = data.split('\t')
            Object.keys(record).forEach((headerName, i) => {
              record[headerName] = eachTdInRow[i]
            })
            
            rowList.push(record)
          }
        })
      })
      return rowList
    })

    console.log(recordList)
    browser.close();

    // Store output
    fs.writeFile('composers.json',JSON.stringify(recordList, null, 2),(err)=>{
      if (err) { console.log(err) }
      else { console.log('Saved Successfully!') }
    })

  } finally {
    await browser.close();
  }
}

initScrape()