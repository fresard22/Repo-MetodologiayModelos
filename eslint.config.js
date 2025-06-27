// eslint.config.js
import globals from "globals";
import tseslint from "typescript-eslint";

// El helper 'tseslint.config' es la forma recomendada de crear la configuración.
// Toma una serie de objetos de configuración y los combina.
export default tseslint.config(
  // 1. Aplica las configuraciones recomendadas base.
  // Esto ya incluye el parser, las reglas base y la definición del plugin.
  ...tseslint.configs.recommended,

  // 2. AÑADE un nuevo objeto para TUS reglas personalizadas.
  // ESTA ES LA PARTE CORREGIDA.
  {
    // Este objeto es nuestra "capa" de personalización.
    // Le decimos que nuestras reglas personalizadas usan el plugin de typescript-eslint.
    plugins: {
      '@typescript-eslint': tseslint.plugin,
    },
    
    // Y aquí definimos las reglas que queremos añadir o sobrescribir.
    rules: {
      // Sobrescribimos una regla del set recomendado para que solo sea una advertencia.
      '@typescript-eslint/no-explicit-any': 'warn',

      // Añadimos una regla de ESLint nativo.
      'no-var': 'error',

      // Añadimos otra regla de ESLint nativo.
      'semi': ['error', 'always'],
    },
  },

  // 3. (Opcional pero recomendado) Un objeto separado para configurar los 'globals'.
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
  }
);