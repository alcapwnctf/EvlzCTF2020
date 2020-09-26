import React, { useState } from 'react';
import { Card, FormGroup, InputGroup, Classes, Button } from '@blueprintjs/core';
import { loginUser, registerUser } from "../api/Api.jsx"
import { withRouter, useHistory, Link } from "react-router-dom";

const loginContainerStyle = {
    display: "flex",
    paddingTop:"0.5rem",
    flexFlow:"row",
    alignItems:"center",
    justifyContent:"center"
}

const formGroupPadding = {
    padding:"0.5rem"
}


function Home() {
    let history = useHistory();

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [organization, setOrganization] = useState("")
    
    async function login(evt) {
        evt.preventDefault()
        try {
            const user = await loginUser({
                username: username,
                password: password,
            })
            if (user.status === 200) {
                history.push(`/user/${user.data.id}`)
            }
        } catch(err) {
            if (err.response) {
                if (err.response.status === 400) {
                    console.log(err.response.data.detail)
                }
            }
        }
    }
    
    async function register() {
        try {
            const user = await registerUser({
                username: username,
                password: password,
                organization: organization
            })
            if (user.status === 200) {
                history.push(`/user/${user.data.id}`)
            }
        } catch(err) {
            if (err.response) {
                if (err.response.status === 400) {
                    console.log(err.response.data.detail)
                }
            }
        }
        
    }
    
    
    return <section style={loginContainerStyle}>
        <Card style={{width:"500px"}}>
            <h1 className={Classes.HEADING}>Login</h1>
            <form>
                <FormGroup 
                    label="Username"
                    style={formGroupPadding}
                >
                    <InputGroup 
                        large
                        required
                        id="username" 
                        onChange={(evt) => {setUsername(evt.target.value)}}
                        placeholder="Enter Username"
                    />  
                </FormGroup>
                <FormGroup 
                    label="Password"
                    style={formGroupPadding}
                >
                    <InputGroup 
                        large
                        required
                        id="password" 
                        onChange={(evt) => setPassword(evt.target.value)}
                        placeholder="Enter password"
                    />  
                </FormGroup>
                <div style={formGroupPadding}>
                    <Button type="submit" onClick={login}>
                        Login
                    </Button>
                </div>
            </form>
            <div>
                <FormGroup 
                    label="Organization"
                    style={formGroupPadding}
                >
                    <InputGroup 
                        large
                        required
                        id="organization"
                        onChange={(evt) => setOrganization(evt.target.value)}
                        placeholder="Name of your organization"
                    />  
                </FormGroup>
                <Button onClick={register}>
                    Register
                </Button>
            </div>
        </Card>
    </section>
}

export default withRouter(Home)
