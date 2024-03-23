const express = require('express');
const app = express();
const PORT = 3000;

let offer = {};

app.use(express.json());

app.get('/oferta', (req, res) => {
    res.json(offer);
});

app.post('/oferta', (req, res) => {
    offer = req.body;
    console.log(offer);

    res.send('oferta recebida');
});

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});