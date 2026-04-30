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
  console.log("Running Broad Search to find ANY receipt... 🤖");

  // This query is much wider to ensure we find a result
  const res = await gmail.users.messages.list({
    userId: 'me',
    q: 'order OR confirmation OR receipt OR delivered OR "thanks for your purchase"', 
    maxResults: 1 
  });

  if (res.data.messages && res.data.messages.length > 0) {
   const message = await gmail.users.messages.get({
      userId: 'me',
      id: res.data.messages[0].id,
      format: 'full' // Get everything!
    });

    // This captures the snippet AND the subject line
    const subject = message.data.payload.headers.find(h => h.name === 'Subject').value;
    const rawText = message.data.snippet;
    
    // Simple extraction for the demo
    const structuredData = {
      platform: rawText.includes("Slikk") ? "Slikk" : "Online Vendor",
      details: rawText.substring(0, 50) + "...",
      status: "Detected",
      timestamp: new Date().toLocaleString()
    };

    console.log("--- ✅ SUCCESS: Data Found ---");
    console.table(structuredData);

    const dbPath = path.join(process.cwd(), 'database.json');
    let currentDb = [];
    try {
        const fileData = await fs.readFile(dbPath, 'utf-8');
        currentDb = JSON.parse(fileData);
    } catch (e) {
        currentDb = [];
    }

    currentDb.push(structuredData);
    await fs.writeFile(dbPath, JSON.stringify(currentDb, null, 2));

    console.log("--- 💾 Saved to database.json ---");
    
  } else {
    console.log("❌ Still no results. This means the search query didn't find a match.");
    console.log("Try checking your Gmail 'Promotions' or 'Updates' tab to see what keywords are there.");
  }
}

startAetherShelfExtraction().catch(console.error);