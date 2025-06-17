import { DataTypes } from 'sequelize';
import sequelize from '../config/db.js';

const Colegio = sequelize.define(
  'colegio',
  {
    codcen: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      allowNull: false,
    },
    nombre: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    regimen: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    direccion: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    CP: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    municipio: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    provincia: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    telef: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    mail: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    latitude: {
      type: DataTypes.FLOAT,
      allowNull: false,
    },
    longitude: {
      type: DataTypes.FLOAT,
      allowNull: false,
    },
  },
  {
    tableName: 'colegios',
    timestamps: false,
    freezeTableName: true,
  }
);

export default Colegio;
