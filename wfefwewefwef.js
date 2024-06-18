const express = require('express');
const bodyParser = require('body-parser');
const libxml = require('libxmljs');
const vm = require('vm');

const app = express();
app.use(bodyParser.text());

function parseXml(xml) {
  return vm.runInContext('libxml.parseXml(xml,{noent:true, noblanks: true, nocdata: true })', xml);
}

app.post('/upload', (req, res) => {
  const xmlData = req.body;
  const xmlDoc = parseXml(xmlData);
  res.json(xmlDoc);
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});



