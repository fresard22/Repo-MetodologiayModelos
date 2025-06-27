# Usa una imagen base de Node
FROM node:20

# Establece el directorio de trabajo
WORKDIR /MateoTutor

# Copia los archivos de definición de dependencias PRIMERO para aprovechar el cache
COPY package.json pnpm-lock.yaml ./

# Instala pnpm y las dependencias
RUN npm install -g pnpm && pnpm install

# Copia el resto del código de tu aplicación
COPY . .

# Expone el puerto 3000
EXPOSE 3000

# Comando para iniciar la aplicación
CMD ["npm", "run", "dev"]