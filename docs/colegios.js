const colegios = {
  '/colegios': {
    get: {
      summary: 'Obtener todos los colegios',
      description: 'Devuelve una lista con todos los colegios',
      responses: {
        200: {
          description: 'Lista de colegios obtenida correctamente',
          content: {
            'application/json': {
              schema: {
                type: 'array',
                items: {
                  $ref: '#/components/schemas/Colegio',
                },
              },
            },
          },
        },
        500: {
          description: 'Error del servidor',
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  message: {
                    type: 'string',
                    example: 'Error del servidor',
                  },
                },
              },
            },
          },
        },
      },
    },
  },
  '/colegios/regimen/{regimen}': {
    get: {
      summary: 'Obtener colegios por régimen',
      description: 'Devuelve todos los colegios que coincidan con el régimen especificado',
      parameters: [
        {
          name: 'regimen',
          in: 'path',
          required: true,
          description: 'Régimen del colegio',
          schema: {
            type: 'string',
            example: 'Público',
          },
        },
      ],
      responses: {
        200: {
          description: 'Colegios encontrados',
          content: {
            'application/json': {
              schema: {
                type: 'array',
                items: {
                  $ref: '#/components/schemas/Colegio',
                },
              },
            },
          },
        },
        404: {
          description: 'No se encontraron colegios',
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  mensaje: {
                    type: 'string',
                    example: 'No se encontraron colegios',
                  },
                },
              },
            },
          },
        },
        500: {
          description: 'Error del servidor',
        },
      },
    },
  },
  '/colegios/municipio/{municipio}': {
    get: {
      summary: 'Obtener colegios por municipio',
      description: 'Devuelve todos los colegios que coincidan con el municipio especificado',
      parameters: [
        {
          name: 'municipio',
          in: 'path',
          required: true,
          description: 'Municipio del colegio',
          schema: {
            type: 'string',
            example: 'Madrid',
          },
        },
      ],
      responses: {
        200: {
          description: 'Colegios encontrados',
          content: {
            'application/json': {
              schema: {
                type: 'array',
                items: {
                  $ref: '#/components/schemas/Colegio',
                },
              },
            },
          },
        },
        404: {
          description: 'No se encontraron colegios',
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  mensaje: {
                    type: 'string',
                    example: 'No se encontraron colegios',
                  },
                },
              },
            },
          },
        },
        500: {
          description: 'Error del servidor',
        },
      },
    },
  },
  '/colegios/nombre/{nombre}': {
    get: {
      summary: 'Buscar colegios por nombre',
      description:
        'Devuelve todos los colegios cuyo nombre contiene el texto proporcionado (insensible a mayúsculas y tildes)',
      parameters: [
        {
          name: 'nombre',
          in: 'path',
          required: true,
          description: 'Texto parcial del nombre del colegio',
          schema: {
            type: 'string',
            example: 'Valencia',
          },
        },
      ],
      responses: {
        200: {
          description: 'Colegios encontrados',
          content: {
            'application/json': {
              schema: {
                type: 'array',
                items: {
                  $ref: '#/components/schemas/Colegio',
                },
              },
            },
          },
        },
        404: {
          description: 'No se encontraron colegios',
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  mensaje: {
                    type: 'string',
                    example: 'No se encontraron colegios con ese nombre',
                  },
                },
              },
            },
          },
        },
        500: {
          description: 'Error del servidor',
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  mensaje: {
                    type: 'string',
                    example: 'Error del servidor',
                  },
                },
              },
            },
          },
        },
      },
    },
  },
};

// Esquema del modelo Colegio
const components = {
  schemas: {
    Colegio: {
      type: 'object',
      properties: {
        codcen: {
          type: 'integer',
          description: 'Código del centro (clave primaria)',
          example: 12345,
        },
        nombre: {
          type: 'string',
          description: 'Nombre del colegio',
          example: 'CEIP Ejemplo',
        },
        regimen: {
          type: 'string',
          description: 'Régimen del colegio',
          example: 'Público',
        },
        direccion: {
          type: 'string',
          description: 'Dirección del colegio',
          example: 'Calle Ejemplo, 123',
        },
        CP: {
          type: 'integer',
          description: 'Código postal',
          example: 28001,
        },
        municipio: {
          type: 'string',
          description: 'Municipio donde se encuentra',
          example: 'Madrid',
        },
        provincia: {
          type: 'string',
          description: 'Provincia donde se encuentra',
          example: 'Madrid',
        },
        telef: {
          type: 'integer',
          description: 'Teléfono de contacto',
          example: 912345678,
        },
        mail: {
          type: 'string',
          description: 'Email de contacto',
          example: 'contacto@ejemplo.edu',
        },
        latitude: {
          type: 'number',
          format: 'float',
          description: 'Latitud de la ubicación',
          example: 40.4168,
        },
        longitude: {
          type: 'number',
          format: 'float',
          description: 'Longitud de la ubicación',
          example: -3.7038,
        },
      },
      required: [
        'codcen',
        'nombre',
        'regimen',
        'direccion',
        'CP',
        'municipio',
        'provincia',
        'telef',
        'mail',
        'latitude',
        'longitude',
      ],
    },
  },
};

export default { paths: colegios, components };
