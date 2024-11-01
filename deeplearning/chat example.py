// Import des modules nécessaires
const express = require('express');
const bodyParser = require('body-parser');

// Initialisation de 
const app = express();
const PORT = 3000;

// Middleware pour traiter les requêtes JSON
app.use(bodyParser.json());

// Route pour le chatbot
app.post('/chatbot', (req, res) => {
    const userMessage = req.body.message;
    const botResponse = getBotResponse(userMessage);
    res.json({ reply: botResponse });
});

// Fonction de réponse du chatbot
function getBotResponse(message) {
    message = message.toLowerCase();

    if (message.includes('bonjour')) {
        return 'Bonjour ! Comment puis-je vous aider ?';
    } else if (message.includes('aide')) {
        return 'Je suis là pour vous aider. Veuillez poser votre question.';
    } else if (message.includes('merci')) {
        return 'De rien ! Si vous avez d’autres questions, n’hésitez pas !';
    } else {
        return 'Je ne comprends pas votre demande. Pouvez-vous reformuler ?';
    }
}

// Démarrage du serveur
app.listen(PORT, () => {
    console.log(`Chatbot démarré sur http://localhost:${PORT}`);
});