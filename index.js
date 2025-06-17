import express from 'express';
import { Sequelize } from 'sequelize';
import 'dotenv/config';

const app = express();
const PORT = process.env.PORT || 3000;
const sequelize = new Sequelize(process.env.DB_URI);

// MIDDLEWARE
app.use(express.json());

// Importa el router de colegios
import colegioRouter from './routes/colegio.js';

// Monta el router de colegios en la ruta /api/colegios
app.use('/api/colegios', colegioRouter);

(async () => {
  try {
    await sequelize.authenticate();
    console.log('Conectado a MySQL');

    app.listen(PORT, () => {
      console.log(`Servidor en http://localhost:${PORT}`);
    });
  } catch (error) {
    console.error('Error al conectar:', error);
    process.exit(1);
  }
})();
