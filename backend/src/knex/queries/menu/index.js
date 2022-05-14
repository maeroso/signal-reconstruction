const knex = require("../../index");

const companyMenu = async function (req) {
  const { companyId } = req.params;
  try {
    const weekday = new Date().getDay() + 1;
    const menu = await knex
      .select(
        "menu.name as menuName",
        "weekday.name as weekdayName",
        "menu_category.name as menuCategoryName",
        "product.productId",
        "product.name as productName",
        "product.description as productDescription",
        "product.price",
        "product_image.name as productImageName"
      )
      .from("menu")
      .innerJoin("weekday_menu", function () {
        this.on("menu.menuId", "=", "weekday_menu.menuId").andOn(
          "menu.companyId",
          "=",
          "weekday_menu.companyId"
        );
      })
      .innerJoin("weekday", function () {
        this.on("weekday.weekdayId", "=", "weekday_menu.weekdayId");
      })
      .innerJoin("menu_product", function () {
        this.on("menu.menuId", "=", "menu_product.menuId").andOn(
          "menu.companyId",
          "=",
          "menu_product.companyId"
        );
      })
      .innerJoin("menu_category", function () {
        this.on(
          "menu_category.menuCategoryId",
          "=",
          "menu_product.menuCategoryId"
        );
      })
      .innerJoin("product", function () {
        this.on("product.productId", "=", "menu_product.productId").andOn(
          "product.companyId",
          "=",
          "menu_product.companyId"
        );
      })
      .leftJoin("product_image", function () {
        this.on("product_image.productId", "=", "menu_product.productId")
          .andOn("product_image.companyId", "=", "menu_product.companyId")
          .andOn("product_image.productImageId", "=", 1);
      })
      .where("menu.companyId", companyId)
      .andWhere("weekday_menu.weekdayId", weekday);
      return menu
  } catch {
    res
      .status(500)
      .json({ message: "500 Internal server error - Error getting menu info" });
  }
};

module.exports = {
  companyMenu,
};
