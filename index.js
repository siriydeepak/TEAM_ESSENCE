const fs = require('fs').promises;
const path = require('path');
const {authenticate} = require('@google-cloud/local-auth');
const {google} = require('googleapis');

async function sayHelloToMailbox() {
  // Use your secret credentials file
  const auth = await authenticate({
    keyfilePath: path.join(process.cwd(), 'credentials.json'),
    scopes: ['https://www.googleapis.com/auth/gmail.readonly'],
  });

  const gmail = google.gmail({version: 'v1', auth});

  // Look for emails with "Blinkit" (Passive Ingestion)
  const res = await gmail.users.messages.list({
    userId: 'me',
    q: 'Blinkit', 
    maxResults: 3
  });

  console.log("Robot is checking the mail... 🤖");
  if (res.data.messages) {
    console.log("Success! I found some receipts!");
  } else {
    console.log("Connected, but no receipts found.");
  }
}

sayHelloToMailbox();