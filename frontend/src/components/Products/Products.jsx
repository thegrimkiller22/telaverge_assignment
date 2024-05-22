// import { Rating } from 'react-simple-star-rating'
import './Products.css'
// import products from '../../ecommerce_db.products';
import { useState, useEffect } from 'react';



const Products = () => {
    const [total, setTotal] = useState(0);
    const [page, setPage] = useState(1);
    const [pageSize] = useState(8);

    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetchData();
        console.log(products)
    }, [page]);

    const fetchData = async () => {
        const response = await fetch(`http://localhost:5000/products?page=${page}&size=${pageSize}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const responseData = await response.json();
        console.log(responseData);
        setTotal(responseData.total);
        const data = responseData.products;
        setProducts(data);
    };



    const handleProductClick = async (id) => {
        console.log(id)
        const user = JSON.parse(localStorage.getItem('loginData'));
        console.log(user._id)

        const element = document.getElementById(id);
        if (element.classList.contains('ri-heart-line')) {
            element.classList.remove('ri-heart-line');
            element.classList.add('ri-heart-fill');
            element.style.color = "red"
            const res = await fetch('http://localhost:5000/record_interaction', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json' // Specify the content type as JSON
                },
                body: JSON.stringify({ user_id: user._id, product_id: id })
            });

            const data = await res.json();
            console.log(data)
        }
        else {
            element.classList.remove('ri-heart-fill');
            element.classList.add('ri-heart-line');
            element.style.color = "black"
            const res = await fetch('http://localhost:5000/delete_interaction', {
                method: "DELETE",
                headers: {
                    'Content-Type': 'application/json' // Specify the content type as JSON
                },
                body: JSON.stringify({ user_id: user._id, product_id: id })
            });

            const data = await res.json();
            console.log(data)
        }
    }
    const handleNextPage = () => {
        if (page < Math.ceil(total / pageSize)) {
            setPage(page + 1);
        }
    };

    const handlePreviousPage = () => {
        if (page > 1) {
            setPage(page - 1);
        }
    };





    return (
        <>

            <div className="products-container">
                <h1 className="heading">Our Products</h1>
                <section className="product-list">
                    {/* Loop through product data and generate product cards */}
                    {products?.map((product) => (
                        <div className="product-card" key={product.name}>
                            <div className="product-card__header">
                                <i id={product._id} className="ri-heart-line like_icon" onClick={() => handleProductClick(product._id)}></i>
                                <div className="product-card__img-container">
                                    <a href={product.link} target='_blank'>
                                        <img src={product.image.replace("/W/IMAGERENDERING_521856-T1/images", "")} alt={product.name} />
                                    </a>
                                </div>
                            </div>
                            <div className="product-card__info">
                                <h3 className="product-title">{product.name}</h3>
                                <div className="product-category">
                                    <li>{product.main_category}</li>
                                    <li>{product.sub_category}</li>
                                </div>
                                <p className="product-price">
                                    <span className="actual">${product['actual_price'].replace('Ã¢â€šÂ¹', '')}</span>
                                    <span className="discount">${product['discount_price'].replace('Ã¢â€šÂ¹', '')}</span>
                                </p>
                                {product.ratings > 0 && <div className="product-rating">
                                    <span className="rating__value">{product.ratings}</span>
                                    <i className='ri-star-fill'></i>
                                    |
                                    <span>{product.no_of_ratings}</span>
                                    {/* <Rating className='rating-stars' initialValue={product.ratings} readonly allowFraction size={20} /> */}

                                </div>}
                            </div>
                        </div>

                        // _id

                        // name

                        // main_category

                        // sub_category

                        // image

                        // link

                        // ratings

                        // no_of_ratings

                        // discount_price

                        // actual_price

                    ))}
                    {/* End of product card loop */}

                </section>
                <div className="pagination-container">
                    <button
                        onClick={handlePreviousPage}
                        disabled={page === 1}
                        className="pagination-button"
                    >
                        Previous
                    </button>
                    <button
                        onClick={handleNextPage}
                        disabled={page >= Math.ceil(total / pageSize)}
                        className="pagination-button"
                    >
                        Next
                    </button>
                    <p className="pagination-text">Page {page} of {Math.ceil(total / pageSize)}</p>
                </div>
            </div>
        </>
    );
}

export default Products;