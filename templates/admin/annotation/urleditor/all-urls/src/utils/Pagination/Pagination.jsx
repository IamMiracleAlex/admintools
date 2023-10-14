import React from 'react';
import Pagination from 'react-js-pagination';
import './Pagination.css';

const Paginations = ({ totalPages, paginate, currentPage, ...rest }) => {
    return (
        <div className="pagination-wrapper">
            <div>
                <Pagination
                    activePage={currentPage}
                    itemsCountPerPage={100}
                    totalItemsCount={totalPages}
                    onChange={paginate}
                />
            </div>
        </div>
    );
};

export default Paginations;
