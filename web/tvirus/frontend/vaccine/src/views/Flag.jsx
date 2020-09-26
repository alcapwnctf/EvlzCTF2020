import React, { useState, useEffect } from 'react';
import { Card, Classes } from '@blueprintjs/core';
import { getFlag } from '../api/Api.jsx'
import { withRouter } from 'react-router-dom';

function Flag() {
    const [flag, setFlag] = useState("")

    useEffect(() => {
        async function initFlag() {
            try {
                const response = await getFlag()
                if (response.status === 200) {
                    setFlag(response.data.flag)
                }
            } catch(err)  {
                if (err.response) {
                    setFlag(err.response.data.detail.error)
                }
            }
        }

        initFlag()
    }, [])
    
    
    return <Card><h1 className={Classes.HEADING}>{flag}</h1></Card>
}

export default withRouter(Flag)
