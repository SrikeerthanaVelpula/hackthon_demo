// server.js
const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.json());

// ------------------- MongoDB Connection -------------------
mongoose.connect("mongodb://127.0.0.1:27017/agriAdvisor", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log("✅ MongoDB Connected"))
.catch(err => console.error("❌ MongoDB Error:", err));

// ------------------- Schema & Model -------------------
const farmerSchema = new mongoose.Schema({
  location: String,
  language: String,
  soilPh: Number,
  soilType: String,
  createdAt: { type: Date, default: Date.now }
});

const Farmer = mongoose.model("Farmer", farmerSchema);

// ------------------- Translations & Recommendations -------------------
const translations = {
  en: {
    recommend: "Recommended Crops & Tips",
    crops: {
      telangana: ["Cotton", "Red Gram (Tur)", "Rice"],
      punjab: ["Wheat", "Rice", "Maize"],
      bihar: ["Maize", "Sugarcane", "Paddy"],
      delhi: ["Vegetables", "Wheat", "Mustard"]
    },
    tips: {
      lowPh: "Add lime to raise soil pH.",
      highPh: "Apply sulfur to reduce alkalinity.",
      sandy: "Add compost to retain water.",
      clay: "Ensure proper drainage.",
      loam: "Balanced soil — maintain organic matter.",
      budget: "Use bio-fertilizers and local seeds to save costs.",
      weather: "Check local rainfall forecast before sowing."
    },
    irrigation: {
      Cotton: { sandy: "Irrigate every 7–10 days.", clay: "Every 15 days.", loam: "Every 12 days." },
      Rice: { sandy: "Needs continuous water.", clay: "Maintain 2–3 inches standing water.", loam: "Keep soil moist, irrigate weekly." }
    }
  },
  hi: {
    recommend: "अनुशंसित फसलें और सुझाव",
    crops: { telangana: ["कपास", "अरहर", "धान"], punjab: ["गेहूं", "धान", "मक्का"], bihar: ["मक्का", "गन्ना", "धान"], delhi: ["सब्ज़ियाँ", "गेहूं", "सरसों"] },
    tips: { lowPh: "मिट्टी की pH बढ़ाने के लिए चुना डालें।", highPh: "क्षारीयता कम करने के लिए गंधक डालें।", sandy: "पानी रोकने के लिए खाद मिलाएँ।", clay: "निकासी सुनिश्चित करें।", loam: "संतुलित मिट्टी — कार्बनिक पदार्थ बनाए रखें।", budget: "जैव उर्वरक और स्थानीय बीज अपनाएँ।", weather: "बुवाई से पहले वर्षा पूर्वानुमान देखें।" }
  }
};

// ------------------- API Routes -------------------

// Save farmer input & return advice
app.post("/get-advice", async (req, res) => {
  const { location, language, soilPh, soilType } = req.body;

  // Save farmer data to DB
  const farmer = new Farmer({ location, language, soilPh, soilType });
  await farmer.save();

  // Get translations
  const t = translations[language] || translations.en;
  const crops = t.crops[location] || [];
  let tipsArr = [];

  if (soilPh < 5.5) tipsArr.push(t.tips.lowPh);
  if (soilPh > 7.5) tipsArr.push(t.tips.highPh);
  if (t.tips[soilType]) tipsArr.push(t.tips[soilType]);
  tipsArr.push(t.tips.budget);
  tipsArr.push(t.tips.weather);

  // Irrigation advice
  let irrigationAdvice = "";
  crops.forEach(crop => {
    if (t.irrigation && t.irrigation[crop] && t.irrigation[crop][soilType]) {
      irrigationAdvice += `💧 ${crop}: ${t.irrigation[crop][soilType]}\n`;
    }
  });

  const message = {
    recommend: t.recommend,
    location,
    crops,
    soilPh,
    soilType,
    tips: tipsArr,
    irrigation: irrigationAdvice
  };

  res.json(message);
});

// Get all farmers history (for dashboard / admin)
app.get("/farmers", async (req, res) => {
  const farmers = await Farmer.find();
  res.json(farmers);
});

// ------------------- Start Server -------------------
const PORT = 5000;
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
