import Colegio from '../models/Colegios.js';
import { Op } from 'sequelize';

const getAllColegios = async (req, res) => {
  try {
    const colegios = await Colegio.findAll();
    res.json(colegios);
  } catch (error) {
    console.error('Error al cargar los colegios', error);
    res.status(500).json({ message: 'Error del servidor' });
  }
};

const getColegiosRegimen = async (req, res) => {
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

const getColegiosMunicipio = async (req, res) => {
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

const getColegiosNombre = async (req, res) => {
  try {
    const colegios = await Colegio.findAll({
      where: { nombre: { [Op.like]: `%${req.params.nombre}%` } },
    });

    res.status(200).json(colegios);
  } catch (error) {
    console.error('Error al obtener el colegio', error);
    res.status(500).json({ mensaje: 'Error del servidor' });
  }
};

export default { getAllColegios, getColegiosRegimen, getColegiosMunicipio, getColegiosNombre };
