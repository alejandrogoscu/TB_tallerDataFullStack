const {sequelize, DataTypes} = require('sequelize');
const sequelize = new sequelize.define ('sqlite::memory:');
const Colegio = sequelize.define('Colegio', {
  nombre: DataTypes.STRING,
  regimen: { type: DataTypes.STRING, allowNull: false },
  direccion: DataTypes.STRING
});
// Endpoint para buscar colegios por régimen
app.get('/api/colegio', async (req, res) => {
  const { regimen } = req.query;
  const where = regimen ? { regimen } : {};
  const colegios = await Colegio.findAll({ where });
  res.json(colegios);
});

const express = require('express');
const router = express.Router();
const Colegio = require('../models/colegio');

// GET: Buscar colegios por municipio (o todos si no se especifica)
router.get('/', async (req, res) => {
  try {
    const { municipio } = req.query;
    const where = municipio ? { municipio } : {};
    const colegios = await Colegio.findAll({ where });
    res.json(colegios);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
