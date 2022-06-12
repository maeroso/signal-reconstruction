const knex = require("../../index");

const application = async function (authorization) {
  let buff = Buffer.from(authorization, "base64");
  authorization = buff.toString("ascii");

  let application = await knex
    .select("applicationId", "name", "redirectUrl")
    .from("application")
    .where("applicationId", authorization);

  if (application.length === 0) {
    application = await knex
      .select(
        "application.applicationId",
        "application.name",
        "application.redirectUrl"
      )
      .from("application")
      .innerJoin("application_access", function () {
        this.on(
          "application.applicationId",
          "=",
          "application_access.applicationId"
        );
      })
      .where("application_access.accessId", authorization);
  }

  return application;
};

const userRoleApplication = async function (authorization, user, password) {
  let buff = Buffer.from(authorization, "base64");
  authorization = buff.toString("ascii");

  let application = await knex
    .select("applicationId", "name as applicationName", "redirectUrl")
    .from("application")
    .where("applicationId", authorization);

  if (application.length === 0) {
    application = await knex
      .select(
        "application.applicationId",
        "application.name as applicationName",
        "application.redirectUrl"
      )
      .from("application")
      .innerJoin("application_access", function () {
        this.on(
          "application.applicationId",
          "=",
          "application_access.applicationId"
        );
      })
      .where("application_access.accessId", authorization);
  }

  const userId = await knex
    .select("user.userId")
    .from("user_role_application")
    .innerJoin("user", function () {
      this.on("user.userId", "=", "user_role_application.userId");
    })
    .where("user.username", user)
    .andWhere("user.password", password)
    .andWhere("user_role_application.applicationId", application[0].applicationId);

  userId[0].application = application;
  return userId
};

module.exports = {
  application,
  userRoleApplication,
};
