import { MagnifyingGlassIcon} from '@heroicons/react/24/solid'
import { useState } from 'react'
const UserInput = ({userInput})=>{
    const [context, setUserText] = useState("")
    const handleClick = (e)=>{
        e.preventDefault()
        const userText = {context}
        fetch('http://localhost:8000/userData', {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(userText)
        })
    }
    return(
        <div className="w-[80%] mx-auto">
            <form className='flex justify-between my-4 border border-gray-400 py-4 rounded-md' onSubmit={(e)=>handleClick(e)}>
                <input 
                    type="text"
                    placeholder="Message Ai Chat"
                    className="pl-4 outline-none w-full"
                    onChange={(e)=>setUserText(e.target.value)}
                />
                <button type='submit'><MagnifyingGlassIcon className='w-8'/></button>
            </form>
            <div>
                {userInput ?.length > 0 ? (
                    <>
                        {userInput.map((Element)=>(
                            <div className='my-4' key={Element.id}>
                                <p  className='border w-fit p-2 rounded-lg bg-accent-lightpurple'>{Element.context}</p>
                            </div>
                        ))}
                    </>):
                (null)
                }
            </div>
        </div>
    )
}

export default UserInput