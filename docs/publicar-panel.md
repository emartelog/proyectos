# Publicar el panel en línea

El panel se puede publicar gratis en [Streamlit Community Cloud](https://share.streamlit.io/)
y queda con un enlace para compartir. Lee los datos de `datos/ultima_corrida/`, así que se
actualiza solo cada vez que el workflow mensual publica un mes nuevo.

1. Entre a [share.streamlit.io](https://share.streamlit.io/) con su cuenta de GitHub y autorice
   el acceso al repositorio.
2. **Create app** → *Deploy a public app from GitHub*.
3. Repositorio: `emartelog/proyectos` (o el repositorio público del proyecto). Rama: la que
   tenga el proyecto. Archivo principal: `panel/app.py`.
4. En *Advanced settings*, Python 3.12.
5. **Deploy.** Las dependencias se instalan desde `panel/requirements.txt`.

Para un enlace fácil de recordar, se puede elegir el subdominio en *App URL*, por ejemplo
`radar-energia.streamlit.app`.
