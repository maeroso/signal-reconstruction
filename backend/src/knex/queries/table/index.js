const knex = require("../../index");

const table = async function (req, res) {
  const { companyId, qrCodeId } = req.params;
  try {
    const table = await knex
      .select(
        "company_table.tableId",
        "company.fantasyName",
      )
      .from("company_table")
      .innerJoin("company", function () {
        this.on("company.companyId", "=", "company_table.companyId");
      })
      .where("company_table.companyId", companyId)
      .andWhere("company_table.qrCodeId", qrCodeId);
      return table
  } catch (err) {
    res
      .status(500)
      .json({ message: "500 Internal server error - Error getting table info", error: err });
  }
};

module.exports = {
  table,
};
