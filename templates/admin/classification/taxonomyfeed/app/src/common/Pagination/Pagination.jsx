import React from 'react';
import ReactPagination from 'react-js-pagination';
import './Pagination.css';

const Pagination = ({ totalPages, paginate, currentPage }) => {
    return (
        <div className="pagination-wrapper">
            <div>
                <ReactPagination
                    activePage={currentPage}
                    itemsCountPerPage={100}
                    totalItemsCount={totalPages}
                    onChange={paginate}
                />
            </div>
        </div>
    );
};

export default Pagination;
