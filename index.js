import express from 'express';
import sequelize from './config/db.js';
import ColegiosRoutes from './routes/colegios.js';
import swaggerUi from 'swagger-ui-express';
import swaggerDocs from './docs/index.js';
import 'dotenv/config';

const app = express();
const PORT = process.env.PORT || 3000;

// MIDDLEWARE
app.use(express.json());

// DOCUMENTACIÓN SWAGGER
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// RUTAS
app.use('/colegios', ColegiosRoutes);

// CONEXIÓN DB Y SERVIDOR
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
