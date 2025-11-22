const express = require('express');
const router = express.Router();
const pool = require('../db');
const { ensureAuth } = require('../utils/authMiddleware');

// Crear mascota
router.post('/', ensureAuth, async (req, res) => {
  const { name, species, breed } = req.body;
  const ownerId = req.user.id;
  const r = await pool.query(
    'INSERT INTO pets (owner_id, name, species, breed) VALUES ($1,$2,$3,$4) RETURNING *',
    [ownerId, name, species, breed]
  );
  res.json(r.rows[0]);
});

// Listar mascotas del usuario
router.get('/', ensureAuth, async (req, res) => {
  const ownerId = req.user.id;
  const r = await pool.query('SELECT * FROM pets WHERE owner_id=$1', [ownerId]);
  res.json(r.rows);
});

module.exports = router;
