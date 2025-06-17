
import basicInfo from './basicinfo.js';
import colegios from './colegios.js';

// Combinamos toda la documentación
const swaggerDocs = {
  ...basicInfo,
  paths: {
    ...colegios.paths
  },
  components: {
    ...colegios.components
  }
};

export default swaggerDocs;