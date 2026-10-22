# Surpan (recuperada desde APK de producción)

Contiene la web compilada (`build/`) y la config de Capacitor (`capacitor.config.json`, appId `es.itop.surpanupgr`).
No incluye el código fuente original (React/Ionic/Vite): solo los bundles minificados.

Recompilar el APK:

    npm install
    npx cap add android
    npx cap sync android
    npx cap open android   # Android Studio -> Build APK

Fijar las versiones de los plugins a las de la app original (ver `capacitor.plugins.json` del APK) y usar tu propio keystore para firmar.
