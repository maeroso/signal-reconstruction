const express = require('express');
const router = express.Router();
const knex = require("../../knex/index");

  router.post('/register', async function(req, res) {
    const { name, email, password } = req.body
    
    const user = await knex
      .select(
        "email"
      )
      .from("users")
      .where("email", email)

    if (user.length > 0) {
      res.status(400).send({ message: 'E-mail já cadastrado' })
    } else {
      try {
        await knex('users').insert(
          {
            name: name.toUpperCase(),
            email: email.toLowerCase(),
            password,
            createdAt: new Date(),  
            updatedAt: new Date(),
          }
        )
        res.status(200).send({ message: 'Usuário criado com sucesso' })
      } catch (error) {
        res.status(500).send({ message: 'Ocorreu um erro inesperado ao criar usuário' })
      }
    }
  })

  router.post('/login', async function(req, res) {
    const { email, password } = req.body
    
    const user = await knex
      .select(
        "name",
        "email",
        "password"
      )
      .from("users")
      .where("email", email.toLowerCase())

    if (user.length === 0) {
      res.status(401).send({ message: 'E-mail ou senha inválido(s)' })
    } else {
      if (user[0].password === password) {
        res.status(200).send({ message: 'Usuário autenticado', name: user[0].name, email: user[0].email })
      } else {
        res.status(401).send({ message: 'E-mail ou senha inválido(s)' })
      }
    }
  })

module.exports = router;