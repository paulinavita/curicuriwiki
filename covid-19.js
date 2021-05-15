const puppeteer = require('puppeteer');
const fs = require('fs')
const scrape = async () =>{
    const browser = await puppeteer.launch({headless : false});
    const page = await browser.newPage();  // opening a new blank page
    await page.goto('https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic_by_country_and_territory', {waitUntil : 'domcontentloaded'}) // navigate to url and wait until page loads completely
   
    const recordList = await page.$$eval('[aria-label="COVID-19 pandemic by country and territory table"] table#thetable tbody tr',(trows)=>{
        let rowList = []    
        trows.forEach(row => {
            let record = {'country' : '','cases' :'', 'death' : '', 'recovered':''}
            record.country = row.querySelector('a').innerText; // (tr < th < a) anchor tag text contains country name
            const tdList = Array.from(row.querySelectorAll('td'), column => column.innerText); // getting textvalue of each column of a row and adding them to a list.
            record.cases = tdList[0];        
            record.death = tdList[1];       
            record.recovered = tdList[2];   
            if(tdList.length >= 3){         
              rowList.push(record)
            }
          });
      return rowList;
    })
    console.log(recordList)
    // await page.screenshot({ path: 'screenshots/wikipedia.png' }); //screenshot 
    browser.close();
    // fs.writeFile('covid-19.json',JSON.stringify(recordList, null, 2),(err)=>{
    //   if (err) {console.log(err)}
    //   else{console.log('Saved!')}
    // })
};
scrape();