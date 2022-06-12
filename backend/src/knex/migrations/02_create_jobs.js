exports.up = function(knex, Promise) {
  return knex.schema.createTable('jobs', function(t) {
      t.increments('id').unsigned().primary();
      t.string('userEmail').notNull();
      t.string('userName').notNull();
      t.string('originalSignalName').notNull();
      t.integer('algorithm').notNull();
      t.integer('signalIncreaseRep').notNull();
      t.integer('iterations').nullable();
      t.integer('status').notNull();
      t.integer('pixelSize').notNull();
      t.dateTime('startTime').nullable();
      t.dateTime('endTime').nullable();
      t.dateTime('createdAt').notNull();
      t.dateTime('updatedAt').notNull();
  });
};

exports.down = function(knex, Promise) {
  return knex.schema.dropTable('jobs')
};