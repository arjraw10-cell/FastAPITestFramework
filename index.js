import express from "express"
const app = express()
app.use(express.json())
app.use(express.static("public"))


app.post("/api/chat", async (req, res) => {
    const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(req.body)
    })

    res.setHeader("Content-Type", "text/plain")

    for await (const chunk of response.body) {
        res.write(chunk)
    }
    res.end()
})


app.listen(3000, () => console.log("Node on 3000"))