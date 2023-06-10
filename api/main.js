const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient } = require('mongodb');

const app = express();
app.use(bodyParser.json());

const mongoURI = 'mongodb://localhost:27017';
const dbName = 'chatApp';
const collectionName = 'chats';

// Store a new chat in MongoDB for a specific UUID
app.post('/chat/:uuid', async (req, res) => {
  try {
    const { uuid } = req.params;
    const { message } = req.body;

    const client = new MongoClient(mongoURI);
    await client.connect();

    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    await collection.insertOne({ uuid, message });

    client.close();

    res.status(201).json({ message: 'Chat stored successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error storing chat' });
  }
});

// Retrieve chat history for a specific UUID from MongoDB
app.get('/chat/:uuid', async (req, res) => {
  try {
    const { uuid } = req.params;

    const client = new MongoClient(mongoURI);
    await client.connect();

    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    const chatHistory = await collection.find({ uuid }).toArray();

    client.close();

    res.status(200).json({ chatHistory });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error retrieving chat history' });
  }
});

// Start the server
app.listen(3000, () => {
  console.log('API server is running on port 3000');
});
