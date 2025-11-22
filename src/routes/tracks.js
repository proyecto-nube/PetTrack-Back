const express = require('express');
const router = express.Router();
const pool = require('../db');
const { ensureAuth } = require('../utils/authMiddleware');

// agregar track a una mascota (propietario solo)
router.post('/:petId', ensureAuth, async (req, res) => {
  const { petId } = req.params;
  const { latitude, longitude, note } = req.body;
  // validamos que la mascota pertenezca al usuario
  const pet = await pool.query('SELECT * FROM pets WHERE id=$1 AND owner_id=$2', [petId, req.user.id]);
  if (!pet.rows.length) return res.status(403).json({ error: 'Not owner or pet not found' });
  const r = await pool.query(
    'INSERT INTO tracks (pet_id, latitude, longitude, note) VALUES ($1,$2,$3,$4) RETURNING *',
    [petId, latitude, longitude, note]
  );
  res.json(r.rows[0]);
});

// obtener tracks de una mascota (propietario)
router.get('/:petId', ensureAuth, async (req, res) => {
  const { petId } = req.params;
  const pet = await pool.query('SELECT * FROM pets WHERE id=$1 AND owner_id=$2', [petId, req.user.id]);
  if (!pet.rows.length) return res.status(403).json({ error: 'Not owner or pet not found' });
  const r = await pool.query('SELECT * FROM tracks WHERE pet_id=$1 ORDER BY created_at DESC', [petId]);
  res.json(r.rows);
});

module.exports = router;
