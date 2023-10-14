import React from 'react';
import { Navbar, Container, NavDropdown, Nav } from 'react-bootstrap';
import { ReactComponent as CentricityLogo } from '../../assets/svg/logo.svg';

const TopNav = () => {
    return (
        <Navbar bg="dark">
            <Container>
                <Navbar.Brand href="/hierarchy">
                    <CentricityLogo />
                </Navbar.Brand>
                <Nav>
                    <NavDropdown
                        className="top-nav__dropdown"
                        title="Users"
                        id="basic-nav-dropdown"
                    >
                        <NavDropdown.Item href="/admin/logout">Logout</NavDropdown.Item>
                    </NavDropdown>
                </Nav>
            </Container>
        </Navbar>
    );
};

export default TopNav;
