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

const getCollegiosRegimen = async (req, res) => {
  try {
    const { regimen } = req.params;
    const colegios = await Colegio.findAll({ where: { regimen } });

    if (colegios.length === 0) {
      return res.status(404).json({ mensaje: 'No se encontraron colegios' });
    }

    res.status(200).json(colegios);
  } catch (error) {
    console.error('Error al obtener el colegio', error);
    res.status(500).json({ mensaje: 'Error del servidor' });
  }
};

const getCollegiosMunicipio = async (req, res) => {
  try {
    const { municipio } = req.params;
    const colegios = await Colegio.findAll({ where: { municipio } });

    if (colegios.length === 0) {
      return res.status(404).json({ mensaje: 'No se encontraron colegios' });
    }

    res.status(200).json(colegios);
  } catch (error) {
    console.error('Error al obtener el colegio', error);
    res.status(500).json({ mensaje: 'Error del servidor' });
  }
};

export default { getAllColegios, getCollegiosRegimen, getCollegiosMunicipio };
