import express from 'express';
import colegio from '../models/Colegios.js'; // Solo una importación, ruta correcta

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    const { municipio } = req.query;
    const where = municipio ? { municipio } : {};
    const colegios = await colegio.findAll({ where }); // Usa la variable importada
    res.json(colegios);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
