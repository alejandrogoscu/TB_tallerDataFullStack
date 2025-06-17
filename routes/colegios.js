import express from 'express';
import ColegioController from '../controllers/ColegioController.js';
const router = express.Router();

router.get('/', ColegioController.getAllColegios);

export default router;
