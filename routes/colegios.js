import express from 'express';
import ColegioController from '../controllers/ColegioController.js';
const router = express.Router();

router.get('/', ColegioController.getAllColegios);
router.get('/regimen/:regimen', ColegioController.getCollegiosRegimen);
router.get('/municipio/:municipio', ColegioController.getCollegiosMunicipio);

export default router;
