import Colegio from '../models/Colegios.js';

const getAllColegios = async (req, res) => {
  try {
    const colegios = await Colegio.findAll();
    res.json(colegios);
  } catch (error) {
    console.error('Error al cargar los colegios', error);
    res.status(500).json({ message: 'Error del servidor' });
  }
};

export default { getAllColegios };
