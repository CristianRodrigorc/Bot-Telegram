# 🚀 Instrucciones de Despliegue en Fly.io

## Prerrequisitos

1. **Instalar Fly CLI**: Descarga desde https://fly.io/docs/hands-on/install-flyctl/
2. **Crear cuenta en Fly.io**: Ve a https://fly.io y regístrate
3. **Iniciar sesión**: Ejecuta `fly auth login`

## Variables de Entorno Necesarias

Tu bot necesita estas APIs:
- **TELEGRAM_TOKEN**: Obtén de @BotFather en Telegram
- **WEATHER_API_KEY**: Obtén de https://openweathermap.org/api
- **NEWS_API_KEY**: Obtén de https://newsapi.org/

## Pasos de Despliegue

### 1. Inicializar la aplicación
```bash
fly launch
```
- Elige un nombre único para tu app (ej: `mi-bot-telegram-123`)
- Selecciona una región cercana
- Cuando pregunte si desplegar ahora, responde **No**

### 2. Configurar variables de entorno
```bash
fly secrets set TELEGRAM_TOKEN=tu_token_aqui WEATHER_API_KEY=tu_api_clima NEWS_API_KEY=tu_api_noticias
```

### 3. Desplegar la aplicación
```bash
fly deploy
```

### 4. Verificar el estado
```bash
fly status
```

### 5. Ver logs (opcional)
```bash
fly logs
```

## Comandos Útiles

- **Reiniciar app**: `fly apps restart`
- **Ver logs en tiempo real**: `fly logs --follow`
- **Escalar**: `fly scale count 1`
- **Destruir app**: `fly apps destroy`

## Solución de Problemas

### Si el bot no responde:
1. Verifica los logs: `fly logs`
2. Asegúrate de que las variables de entorno estén configuradas: `fly secrets list`
3. Reinicia la app: `fly apps restart`

### Si hay errores de build:
1. Verifica que el Dockerfile esté correcto
2. Asegúrate de que requirements.txt tenga todas las dependencias
3. Revisa que no haya archivos innecesarios en .dockerignore

## Notas Importantes

- El bot se ejecutará continuamente en Fly.io
- Las variables de entorno están seguras y no se exponen en el código
- Puedes actualizar el bot con `fly deploy` cada vez que hagas cambios
- Fly.io ofrece un plan gratuito generoso para bots pequeños
