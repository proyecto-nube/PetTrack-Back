const express = require('express');
const router = express.Router();
const pool = require('../db');
const bcrypt = require("bcryptjs");
const jwt = require('jsonwebtoken');
const SECRET = process.env.JWT_SECRET || 'un_secretito_local';

router.post('/register', async (req, res) => {
  const { email, password, name } = req.body;
  if (!email || !password) return res.status(400).json({ error: 'email & password required' });
  try {
    const hashed = await bcrypt.hash(password, 10);
    const result = await pool.query(
      'INSERT INTO users (email, password, name) VALUES ($1,$2,$3) RETURNING id, email, name',
      [email, hashed, name]
    );
    const user = result.rows[0];
    const token = jwt.sign({ id: user.id, email: user.email }, SECRET, { expiresIn: '7d' });
    res.json({ user, token });
  } catch (err) {
    if (err.code === '23505') return res.status(400).json({ error: 'Email already exists' });
    console.error(err);
    res.status(500).json({ error: 'server error' });
  }
});

router.post('/login', async (req, res) => {
  const { email, password } = req.body;
  const result = await pool.query('SELECT id, email, password, name FROM users WHERE email=$1', [email]);
  const user = result.rows[0];
  if (!user) return res.status(401).json({ error: 'invalid credentials' });
  const ok = await bcrypt.compare(password, user.password);
  if (!ok) return res.status(401).json({ error: 'invalid credentials' });
  const token = jwt.sign({ id: user.id, email: user.email }, SECRET, { expiresIn: '7d' });
  res.json({ user: { id: user.id, email: user.email, name: user.name }, token });
});

module.exports = router;
