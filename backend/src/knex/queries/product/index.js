const knex = require("../../index");

const productDetail = async function (req) {
  const { companyId, productId } = req.params;
  const product = await knex
    .select('product.productId', 'product.companyId', 'product.name', 'product.description', 'product.price')
    .from('product')
    .where('product.companyId', companyId)
    .andWhere('product.productId', productId)
  
    const images = await knex
    .select('product_image.name')
    .from('product_image')
    .where('product_image.companyId', companyId)
    .andWhere('product_image.productId', productId)

    product[0].images = images
    return product
}

const products = async function (req) {
  const { companyId } = req.params;
  return knex
    .select('product.productId', 'product.companyId', 'product.name', 'product.description', 'product.price', 'product_image.name as productImageName')
    .from('product')
    .leftJoin('product_image', function () {
      this.on('product_image.productId', '=', 'product.productId')
      .andOn('product_image.companyId', '=', 'product.companyId')
      .andOn('product_image.productImageId', '=', 1)
    })
    .where('product.companyId', companyId)
}

module.exports = {
  products,
  productDetail,
}