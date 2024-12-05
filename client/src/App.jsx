import { useEffect, useState } from "react"
import UserInput from "./userInput"

function App() {
  const [userData, setUserData ] = useState([])
  const getData = async ()=>{
    const res = await fetch("http://localhost:8000/userData")
    const data = await res.json()
    console.log(data)
    setUserData(data)
  }

 useEffect(()=>{
  getData()
 }, [])

  return (
    <>
      <UserInput 
        userInput={userData}
      />
    </>
  )
}

export default App
