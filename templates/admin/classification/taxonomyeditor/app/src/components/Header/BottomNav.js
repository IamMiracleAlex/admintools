import React from 'react';

const BottomNav = () => {
    return (
        <ul className='nav nav-pills custom-nav-pills'>
            <div className='container px-0 d-flex'>
                <li className='nav-item '>
                    <a className=' nav-link active pl-0' href='/admin'>
                        Admin Dashboard
                    </a>
                </li>
                <li className='nav-item'>
                    <a className='nav-link px-5' href='/hierarchy/'>
                        Hierarchy
                    </a>
                </li>
            </div>
        </ul>
    );
};

export default BottomNav;
