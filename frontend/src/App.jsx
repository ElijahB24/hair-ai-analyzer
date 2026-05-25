import { useState } from 'react'

function App() {

  //store selected image file
  const [file, setFile] = useState(null)

  //store image preview URL
  const [preview, setPreview] = useState(null)
  
  //store prediction results
  const [results, setResults] = useState(null)

  //loading state
  const [loading, setLoading] = useState(false)

  //handle image upload
  const handleFileChange = (event) => {

    const selectedFile = event.target.files[0]
    setFile(selectedFile)

    //creates preview URL for selected image
    if (selectedFile) {
      setPreview(URL.createObjectURL(selectedFile)) //create image preview
    }
  }

  //send image to backend
  const handleUpload = async () => {

    //checker for existence of file
    if (!file) {
      alert('Please select an image file first.')
      return
    }

    setLoading(true)

    //create form data to send file
    const formData = new FormData()
    formData.append('file', file)

    try {
      //send POST request to FastAPI
      const response = await fetch("http://127.0.0.1:8000/predict",
        {method: 'POST', body: formData}
      )

      //convert response to JSON
      const data = await response.json()

      //save production result
      setResults(data)

    } catch (error) {
      alert('Error connecting to backend: ' + error.message)
    }

    setLoading(false)
  }

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#0f172a",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      fontFamily: "Arial"
    }}>

      <div style={{
        backgroundColor: "#1e293b",
        padding: "40px",
        borderRadius: "20px",
        width: "400px",
        textAlign: "center",
        boxShadow: "0px 0px 20px rgba(0,0,0,0.4)"
      }}>

        <h1 style={{
          color: "white",
          marginBottom: "10px"
        }}>
          Hair AI Analyzer
        </h1>

        <p style={{
          color: "#cbd5e1",
          marginBottom: "30px"
        }}>
          Upload an image to analyze hair type
        </p>

        {/* Image Preview */}
        {preview && ( //only show preview if an image exists

          <img
            src={preview}
            alt="Preview"
            style={{
              width: "300px",
              height: "300px",
              objectFit: "cover",
              objectPosition: "top",
              borderRadius: "15px",
              marginBottom: "20px",
              border: "2px solid #475569"
            }}
          />
        )}

        {/* File Input */}
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          style={{
            marginBottom: "20px",
            color: "white"
          }}
        />

        <br />

        {/* Predict Button */}
        <button
          onClick={handleUpload}

          style={{
            backgroundColor: "#3b82f6",
            color: "white",
            border: "none",
            padding: "12px 24px",
            borderRadius: "10px",
            cursor: "pointer",
            fontSize: "16px",
            fontWeight: "bold"
          }}
        >

          {loading ? "Analyzing..." : "Predict Hair Type"}

        </button>

        {/* Results */}
        {results && (

          <div style={{
            marginTop: "30px",
            backgroundColor: "#334155",
            padding: "20px",
            borderRadius: "15px"
          }}>

            <h2 style={{
              color: "white"
            }}>
              Prediction: {results.prediction}
            </h2>

            <h3 style={{
              color: "#93c5fd"
            }}>
              Confidence: {results.confidence}%
            </h3>

          </div>
        )}

      </div>

    </div>
  )
}

export default App
