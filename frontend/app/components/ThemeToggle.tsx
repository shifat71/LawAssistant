import React, { useContext } from 'react'
import { ThemeContext } from '../contextProvider/ThemeContextProvider'

const ThemeToggle = () => {

    const { theme, toggle } = useContext(ThemeContext);
    return (
        <div onClick={toggle}>
            Theme: {theme}
        </div>
    )
}

export default ThemeToggle
