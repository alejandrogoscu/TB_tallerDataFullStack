const {sequelize, DataTypes} = require('sequelize');
const sequelize = new sequelize.define ('sqlite::memory:');
const Colegio = sequelize.define('Colegio', {
  nombre: DataTypes.STRING,
  regimen: { type: DataTypes.STRING, allowNull: false },
  direccion: DataTypes.STRING
});
// Endpoint para buscar colegios por régimen
app.get('/api/colegios', async (req, res) => {
  const { regimen } = req.query;
  const where = regimen ? { regimen } : {};
  const colegios = await Colegio.findAll({ where });
  res.json(colegios);
});