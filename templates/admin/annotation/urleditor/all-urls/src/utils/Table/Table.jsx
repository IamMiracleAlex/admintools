import React from 'react';
import TableHead from './TableHead/TableHead';
import TableBody from './TableBody/TableBody';
import './Table.css';

const Table = ({ headers = [], dataSource = [] }) => {
    return (
        <div className="table-responsive">
            <table className="table table-bordered">
                <TableHead headers={headers} />
                <TableBody dataSource={dataSource} />
            </table>
        </div>
    );
};

export default Table;
