import React, { useEffect, useState } from 'react';

const Clock: React.FC = () => {
    const now = new Date();
    const [currentTime, setCurrentTime] = useState<string>(now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
    }))

    useEffect(() => {
        const timeout = setInterval(() => {
        const now = new Date()
        setCurrentTime(now.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            second: '2-digit'
        }))
        }, 1000)
    
        return () => clearInterval(timeout)
    }, [])

    return <p className="text-lg font-semibold text-primary">{currentTime}</p>
}

export default Clock;