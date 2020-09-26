import React from 'react';
import { Navbar, Alignment, Button } from '@blueprintjs/core'
import { Link } from 'react-router-dom'

function TopBar() {
    return (
        <>
        <Navbar>
            <Navbar.Group align={Alignment.LEFT}>
                <Navbar.Heading>Vaccine Builders</Navbar.Heading>
                <Navbar.Divider />
                <Link to="/">
                <Button className="bp3-minimal" icon="home" text="Home" />
                </Link>
            </Navbar.Group>
        </Navbar>
        </>
    );
}

export default TopBar;
