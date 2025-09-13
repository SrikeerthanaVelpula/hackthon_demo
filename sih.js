async function getAdvice(phInput, soilInput) {
  const location = document.getElementById("location").value;
  const language = document.getElementById("language").value;
  const soilPh = phInput || parseFloat(document.getElementById("soilPh").value);
  const soilType = soilInput || document.getElementById("soilType").value;

  const response = await fetch("http://localhost:5000/get-advice", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ location, language, soilPh, soilType })
  });

  const data = await response.json();

  const msg = 
    `${data.recommend}:\n\n📍 ${data.location}\n` +
    `🌾 ${data.crops.join(", ")}\n\n` +
    `🧪 Soil pH: ${data.soilPh}, Type: ${data.soilType}\n\n` +
    `➤ ${data.tips.join("\n➤ ")}\n\n` +
    `💧 Irrigation Advice:\n${data.irrigation}`;

  document.getElementById("adviceBox").innerText = msg;
  currentAdvice = msg;
}
