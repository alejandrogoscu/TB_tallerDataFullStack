import express from 'express';
import ColegioController from '../controllers/ColegioController.js';
const router = express.Router();

router.get('/', ColegioController.getAllColegios);
router.get('/regimen/:regimen', ColegioController.getColegiosRegimen);
router.get('/municipio/:municipio', ColegioController.getColegiosMunicipio);
router.get('/nombre/:nombre', ColegioController.getColegiosNombre);

export default router;
