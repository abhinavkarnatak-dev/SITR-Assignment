require("dotenv").config(); // Load environment variables

const axios = require("axios");
const { MongoClient } = require("mongodb");

// MongoDB connection setup
const client = new MongoClient(process.env.MONGO_URI);

let db, collection;

client
  .connect()
  .then(() => {
    console.log("Connected to MongoDB");
    db = client.db("Twitter");
    collection = db.collection("trending");
  })
  .catch((err) => {
    console.error("MongoDB connection error:", err);
  });

const triggerScrapingAndSave = async () => {
  try {
    const response = await axios.get(process.env.PYTHON_SERVER_URL);
    console.log("Scraping triggered:", response.data);

    const { trends, ip_address } = response.data;

    const data = {
      trend1: trends[0],
      trend2: trends[1],
      trend3: trends[2],
      trend4: trends[3],
      trend5: trends[4],
      date_time: new Date(),
      ip_address,
    };

    await collection.insertOne(data);
    console.log("Data inserted into MongoDB");
  } catch (error) {
    console.error("Error during scraping:", error);
  }
};

const getLatestScrapingData = async (req, res) => {
  try {
    const latestRecord = await collection
      .find()
      .sort({ date_time: -1 })
      .limit(1)
      .toArray();

    res.json({
      message: `These are the most happening topics as of ${latestRecord[0].date_time}`,
      trends: [
        latestRecord[0].trend1,
        latestRecord[0].trend2,
        latestRecord[0].trend3,
        latestRecord[0].trend4,
        latestRecord[0].trend5,
      ],
      ip_address: latestRecord[0].ip_address,
      mongo_data: latestRecord[0],
    });
  } catch (error) {
    console.error("Error fetching scraping data:", error);
    res.status(500).send("Error during scraping");
  }
};

module.exports = {
  triggerScrapingAndSave,
  getLatestScrapingData,
};