const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const scrapingRoutes = require("./routes/scraping");
const path = require("path");

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static("server/public"));
app.use("/api/scraping", scrapingRoutes);

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});