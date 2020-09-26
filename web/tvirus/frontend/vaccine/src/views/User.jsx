import React, { useState, useEffect } from 'react';
import { Card, FormGroup, InputGroup, TextArea, Classes, Button } from '@blueprintjs/core';
import { withRouter, useRouteMatch, Link } from "react-router-dom";
import { getUser, createVaccine, getPreview } from '../api/Api.jsx';

const userContainerStyle = {
    display: "flex",
    width:"100%",
    padding:"0.5rem",
    flexFlow:"row",
}

function User() {
    const match = useRouteMatch()
    const user_id = match.params.id
    
    const [userResponse, setUserResponse] = useState(undefined)
    const [preview, setPreview] = useState(<></>)
    const [description, setDescription] = useState("")
    
    async function initUser() {
        try {
            const user = await getUser(user_id)
            if (user.status === 200) {
                setUserResponse(user)
            }
        } catch(err) {
            if (err.response) {
                if (err.response.status === 400) {
                    console.log(err.response.data.detail)
                }
            }
        }
    }
    
    useEffect(() => {
        const init = async () => {
            initUser()
        }
        init()
    }, [])

    async function newVaccine(evt) {
        evt.preventDefault()
        let name = evt.target.name.value
        let description = evt.target.description.value
        try {
            const user = await createVaccine(user_id, {
                name: name,
                description: description
            })

            if (user.status === 200) {
                setUserResponse(user)
            }
        } catch(err) {
            console.log(err.response)    
        }
    }

    async function generatePreview() {        
        const getUrl = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/g
        const urls = description.match(getUrl)
        
        if (urls !== null) {
            if (urls.length === 0) {
                return
            }
        } else {
            return
        }
        
        try { 
            const url = encodeURI(urls.slice(-1)[0])
            const previewResponse = await getPreview(url)
            if (previewResponse.status === 200) {
                setPreview(<><Card style={{padding:"1rem"}}><p>{previewResponse.data.title}</p><br /><p>{previewResponse.data.text.substring(0, 100)}</p></Card></>)
            }
        } catch (err) {
            if (err.response) {
                setPreview(<>{err.response.data.detail.error}</>)
            }
        }
        
    }
    
    return <>
    <section style={userContainerStyle}>
        <Card>
            { userResponse ? <>
                <h1 className={Classes.HEADING}>{userResponse.data.username}</h1>
                <h2 className={Classes.HEADING}>{userResponse.data.organization}</h2>
                <h4 className={Classes.HEADING}>{userResponse.data.is_admin ? "Admin" : "User"}</h4>
                <Link to="/flag">Get Flag!</Link>
            </> : <></>}    
        </Card>
        <div style={{display:"flex", flexFlow:"column", width:"100%", paddingLeft:"1rem"}}>
            <h1 className={Classes.HEADING}>Vaccines</h1>
            <div style={{display:"inline", width:"50%"}}>
                <form onSubmit={newVaccine}>
                    <FormGroup
                        label="Vaccine Name"
                    >
                        <InputGroup
                            id="name"
                        />
                    </FormGroup>
                    <FormGroup
                        label="Vaccine Description"
                    >
                        <TextArea
                            style={{width:"100%"}}
                            id="description"
                            onChange={(chg) => setDescription(chg.target.value)}
                        />
                        <div style={{paddingTop:"0.5rem"}}>
                            <Button onClick={generatePreview}>
                                Generate Link Preview
                            </Button>
                        </div>
                        <div style={{paddingTop:"0.5rem"}}>
                            {preview}
                        </div>
                    </FormGroup>
                    <Button type="submit">
                        Create Vaccine
                    </Button>
                </form>
            </div>
        </div>
    </section>
    { userResponse ? <><div style={{display:"flex", flexFlow:"row wrap"}}>{userResponse.data.vaccines.map((vacc) => {
        return <Card style={{width:"30%", margin:"1rem"}}><h3 className={Classes.HEADING}>{vacc.name}</h3><h6 className={Classes.HEADING}>{vacc.description}</h6><p>Approved: {vacc.approved ? "Yes" : "No"}</p></Card>
    })}</div></> : <></>}
    </>
}

export default withRouter(User)
