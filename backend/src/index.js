const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser')
const app = express()
const port = 3333

app.use(cors())

app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())

app.post('/upload', (req, res) => {
  const { g } = req.body
  res.send(g)
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

