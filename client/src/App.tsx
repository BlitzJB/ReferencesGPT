import { Results } from "./Results"
import { useState, useRef } from "react"

function App() {
  const [results, setResults] = useState([])
  const [fetching, setFetching] = useState(false)
  const [error, setError] = useState("")
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const status = error ? "error" : fetching ? "loading" : "success"

  async function handleClick() {
    const input = inputRef.current?.value
    if (input === undefined) return
    if (input === "") {
      alert("Please enter some text")
      return
    }
    setFetching(true)
    setError("")
    const response = await fetch("https://blitz-model-service.jb2k4.repl.co/api/research", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: input
      })
    })
    if (!response.ok) {
      setError("Something went wrong")
      console.log(await response.text())
      setFetching(false)
      return
    }
    const data = await response.json()
    setResults(data)
    setFetching(false)
  }

  return (
    <div className="h-screen relative">
      <nav className="py-10 px-5 lg:px-20 box-border flex items-center">
        <h1 className="text-2xl font-bold">
          ReferencesGPT
        </h1>
        <button onClick={_ => handleClick()} className={"text-neutral-100 px-4 py-2 rounded-sm ml-auto " + (fetching ? "bg-neutral-500 cursor-not-allowed" : "bg-neutral-700")}>
          {
            fetching ? "Please Wait" : "Search"
          }
        </button>
      </nav>
      <main className="flex flex-grow lg:h-[calc(100%-120px)] lg:px-20 px-5 pb-10 flex-col lg:flex-row box-border">
        <div className="lg:w-2/5 w-full lg:h-full h-[70vh] lg:mx-2 border border-neutral-500 relative rounded-md">
          <textarea ref={inputRef} disabled={fetching} className={"h-full w-full p-3 resize-none bg-transparent rounded-md subtle-scrollbar" + (fetching ? " cursor-not-allowed" : "")} placeholder="Start typing here..."></textarea>
        </div>
        <h3 className="lg:hidden mt-5 font-bold">Results</h3>
        <div className="lg:w-3/5 w-full h-full lg:mx-2 mt-3 lg:mt-0 p-3 pt-0 overflow-y-scroll subtle-scrollbar border border-neutral-500 rounded-md">
          <Results results={results} status={status} error={error} />
        </div>
      </main>
    </div>
  )
}

export default App
