require('dotenv').config();
const express = require('express');
const cors = require('cors');
const app = express();
const authRoutes = require('./routes/auth');
const petsRoutes = require('./routes/pets');
const tracksRoutes = require('./routes/tracks');

app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/pets', petsRoutes);
app.use('/api/tracks', tracksRoutes);

const port = process.env.PORT || 4000;
app.listen(port, () => {
  console.log('Backend running on port', port);
});
