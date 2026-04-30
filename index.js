const fs = require('fs').promises;
const path = require('path');
const {authenticate} = require('@google-cloud/local-auth');
const {google} = require('googleapis');

async function startAetherShelfExtraction() {
  const auth = await authenticate({
    keyfilePath: path.join(process.cwd(), 'credentials.json'),
    scopes: ['https://www.googleapis.com/auth/gmail.readonly'],
  });

  const gmail = google.gmail({version: 'v1', auth});
  console.log("Hunting for Blinkit, Amazon, and Zomato receipts... 🤖");

  // Search for the latest receipt from your target apps
  const res = await gmail.users.messages.list({
    userId: 'me',
    q: '(from:blinkit.com OR from:zomato.com OR from:amazon.in) "Order Summary" OR "Order Confirmation" OR "Order delivered"', 
    maxResults: 1 
  });

  if (res.data.messages && res.data.messages.length > 0) {
    const message = await gmail.users.messages.get({
      userId: 'me',
      id: res.data.messages[0].id,
    });

    const rawText = message.data.snippet.toLowerCase();
    
    // --- THE MULTI-PLATFORM BRAIN ---
    let platform = "Unknown Vendor";
    if (rawText.includes("blinkit")) platform = "Blinkit";
    else if (rawText.includes("zomato")) platform = "Zomato";
    else if (rawText.includes("amazon")) platform = "Amazon";

    // Attempt to extract an Order ID or Price (Passive Ingestion)
    const orderIdMatch = rawText.match(/(?:order #|id:?|order id:?)\s*([a-z0-9-]+)/i);
    const priceMatch = rawText.match(/(?:rs\.?|₹)\s*(\d+(?:\.\d{2})?)/i);

    const structuredData = {
      platform: platform,
      orderId: orderIdMatch ? orderIdMatch[1].toUpperCase() : "Searching...",
      estimatedTotal: priceMatch ? `₹${priceMatch[1]}` : "Check full email",
      status: "Detected",
      timestamp: new Date().toLocaleString()
    };

    console.log("--- ✨ SUCCESS: Receipt Data Found ---");
    console.table(structuredData);
    console.log("---------------------------------------");
    console.log("Next Step: Connecting this to your MongoDB/AuraHealth backend!");
  } else {
    console.log("❌ No recent receipts found for Blinkit, Amazon, or Zomato.");
    console.log("Tip: Ensure you have an 'Order Summary' email in your inbox from one of these.");
  }
}

startAetherShelfExtraction().catch(console.error);