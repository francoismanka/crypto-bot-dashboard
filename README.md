
# Crypto Bot Dashboard (Render Ready)

Ce projet contient :
- `server.py` : un serveur Flask qui héberge le tableau de bord.
- `templates/dashboard.html` : la page web du tableau de bord.
- `bot_pro.py` : le bot qui envoie les données au tableau de bord.

## Déploiement sur Render (en 3 étapes) :
1. Crée un compte sur [https://render.com](https://render.com).
2. Clique sur **New +** > **Web Service**.
3. Connecte ton dépôt GitHub contenant ces fichiers, choisis Python 3 et mets la commande de démarrage :  
   ```
   python server.py
   ```

Ton tableau de bord sera alors accessible via une URL publique (exemple : https://monbot.onrender.com).
