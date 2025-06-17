
const basicInfo = {
  openapi: "3.1.0",
  info: {
    title: "Colegios API",
    version: "1.0.0",
    description: "API simple para gestionar colegios"
  },
  servers: [
    {
      url: "http://localhost:3000",
      description: "Servidor de desarrollo"
    },
    {
      url: "https://tb-tallerdatafullstack.onrender.com",
      description: "Servidor de producción"
    }
  ]
};

export default basicInfo;