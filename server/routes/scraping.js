const express = require('express');
const scrapingController = require('../controllers/scrapingController');

const router = express.Router();

router.get('/run-scraping', async (req, res) => {
  try {
    await scrapingController.triggerScrapingAndSave();
    res.status(200).send('Scraping triggered and data saved!');
  } catch (error) {
    res.status(500).send('Error during scraping');
  }
});

router.get('/latest-scraping-data', scrapingController.getLatestScrapingData);

module.exports = router;
