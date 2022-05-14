exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return knex('users').del()
  .then(function () {
    // Inserts seed entries
    return knex('users').insert([
      {
        name: 'Lucas Giovanni de Castro Ribeiro'.toUpperCase(),
        email: 'lucas.giovannicr@gmail.com',
        password: 'lucasribeiro',
        createdAt: new Date(),  
        updatedAt: new Date(),
      },
      {
        name: 'José Moscardi da Silva Junior'.toUpperCase(),
        email: 'jmoscajr@gmail.com',
        password: '123456',
        createdAt: new Date(),  
        updatedAt: new Date(),
      },
    ]);
  });
};