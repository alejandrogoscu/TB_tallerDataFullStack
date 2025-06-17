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

console.log('¿Swagger docs existe?', !!swaggerDocs);
console.log('Swagger docs keys:', Object.keys(swaggerDocs || {}));

// Después de las líneas anteriores, agregar:
console.log('Configurando ruta /api-docs...');

app.use(
  '/api-docs',
  (req, res, next) => {
    console.log('Acceso a /api-docs detectado');
    next();
  },
  swaggerUi.serve,
  swaggerUi.setup(swaggerDocs)
);

console.log('Ruta /api-docs configurada');

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
