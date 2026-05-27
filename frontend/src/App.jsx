import { useState, useRef, useEffect } from 'react'
import { useDropzone } from 'react-dropzone'
import Webcam from 'react-webcam'

function App() {

  // Store uploaded image file
  const [file, setFile] = useState(null)

  // Store image preview URL
  const [preview, setPreview] = useState(null)

  // Store prediction results
  const [results, setResults] = useState(null)

  // Loading state
  const [loading, setLoading] = useState(false)

  //webcam reference
  const webcamRef = useRef(null)
  //toggle webcam
  const [showWebcam, setShowWebcam] = useState(false)

  // Runs when image is uploaded
  const onDrop = (acceptedFiles) => {

    // Get uploaded image
    const selectedFile = acceptedFiles[0]

    // Save uploaded image
    setFile(selectedFile)

    // Create preview URL
    if (selectedFile) {

      setPreview(
        URL.createObjectURL(selectedFile)
      )
    }
  }

  // Create drag/drop upload area
  const {
    getRootProps,
    getInputProps
  } = useDropzone({

    // Run on image upload
    onDrop,

    // Only allow image files
    accept: {
      'image/*': []
    }
  })

  // Send image to backend
  const handleUpload = async () => {

    // Check if image exists
    if (!file) {

      alert('Please select an image first.')

      return
    }

    // Turn loading on
    setLoading(true)

    // Create form data
    const formData = new FormData()

    formData.append('file', file)

    try {

      // Send image to backend
      const response = await fetch(
        'http://127.0.0.1:8000/predict',
        {
          method: 'POST',
          body: formData
        }
      )

      // Convert response to JSON
      const data = await response.json()

      // Save prediction results
      setResults(data)

    } catch (error) {

      alert(
        'Error connecting to backend: '
        + error.message
      )
    }

    // Turn loading off
    setLoading(false)
  }

  //continuously scan using webcam
  const scanFrame = async () => {

    // make sure webcam exists
    if (!webcamRef.current) return

    // capture current webcam frame
    const imageSrc =
      webcamRef.current.getScreenshot()

    // stop if frame failed
    if (!imageSrc) return

    try {

      // convert webcam image into blob
      const response = await fetch(imageSrc)

      const blob = await response.blob()

      // convert blob into image file
      const webcamFile = new File(
        [blob],
        "webcam.jpg",
        {
          type: "image/jpeg"
        }
      )

      // create form data
      const formData = new FormData()

      formData.append("file", webcamFile)

      // send webcam frame to backend
      const predictionResponse =
        await fetch(
          "http://127.0.0.1:8000/predict",
          {
            method: "POST",
            body: formData
          }
        )

      // convert prediction to JSON
      const data =
        await predictionResponse.json()

      // update predictions live
      setResults(data)

    } catch (error) {

      console.log(
        "Live scanner error:",
        error
      )
    }
  }

  // run live scanner repeatedly
  useEffect(() => {

    let interval

    // only scan if webcam enabled
    if (showWebcam) {

      // wait briefly for webcam to initialize
      setTimeout(() => {

        interval = setInterval(() => {

          scanFrame()

        }, 1000) // scan every second

      }, 1500)
    }

    // cleanup interval
    return () => {

      if (interval) {
        clearInterval(interval)
      }
    }

  }, [showWebcam])

  return (

    <div style={{
      minHeight: '100vh',
      backgroundColor: '#0f172a',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      fontFamily: 'Arial'
    }}>

      <div style={{
        backgroundColor: '#1e293b',
        padding: '40px',
        borderRadius: '20px',
        width: '400px',
        textAlign: 'center',
        boxShadow: '0px 0px 20px rgba(0,0,0,0.4)'
      }}>

        <h1 style={{
          color: 'white',
          marginBottom: '30px'
        }}>
          Hair AI Analyzer
        </h1>

        <p style={{
          color: '#cbd5e1',
          marginBottom: '30px'
        }}>
          Upload an image to analyze hair type
        </p>

        {/* Image Preview */}
        {preview && (

          <img
            src={preview}
            alt="Preview"

            style={{
              width: '300px',
              height: '300px',
              objectFit: 'cover',
              objectPosition: 'top',
              borderRadius: '15px',
              marginBottom: '20px',
              border: '2px solid #475569'
            }}
          />
        )}

        {/* Drag and Drop Upload Area */}
        <div

          // Enable drag/drop behavior
          {...getRootProps()}

          style={{
            border: '2px dashed #475569',
            padding: '30px',
            borderRadius: '15px',
            cursor: 'pointer',
            color: 'white',
            marginBottom: '20px',
            backgroundColor: '#334155'
          }}
        >

          {/* Hidden file input */}
          <input {...getInputProps()} />

          <p>
            Drag & Drop an image here
          </p>

          <p style={{
            color: '#94a3b8',
            fontSize: '14px'
          }}>
            or click to browse
          </p>

        </div>
        {/* Webcam Scanner Button */}
        <button

          onClick={() =>
            setShowWebcam(!showWebcam)
          }

          style={{
            backgroundColor: "#475569",
            color: "white",
            border: "none",
            padding: "10px 20px",
            borderRadius: "10px",
            cursor: "pointer",
            marginBottom: "20px"
        }}
      >

        {showWebcam
          ? "Stop Scanner"
          : "Start Live Scanner"}

      </button>

            {/* Live Webcam */}
      {showWebcam && (

        <Webcam

          ref={webcamRef}

          audio={false}

          mirrored={true}

          screenshotFormat="image/jpeg"

          videoConstraints={{
            width: 1280,
            height: 720,
            facingMode: "user"
          }}

          style={{
            width: '100%',
            height: '300px',
            objectFit: 'cover',
            borderRadius: '15px',
            marginBottom: '20px',
            border: '2px solid #475569',
            backgroundColor: 'black'
          }}
        />
      )}

        {/* Predict Button */}
        <button

          onClick={handleUpload}

          style={{
            backgroundColor: '#3b82f6',
            color: 'white',
            border: 'none',
            padding: '12px 24px',
            borderRadius: '10px',
            cursor: 'pointer',
            fontSize: '16px',
            fontWeight: 'bold'
          }}
        >

          {loading
            ? 'Analyzing...'
            : 'Predict Hair Type'
          }

        </button>

        {/* Results */}
        {results && (

          <div style={{
            marginTop: '30px',
            backgroundColor: '#334155',
            padding: '20px',
            borderRadius: '15px'
          }}>

            {/* Prediction */}
            <h2 style={{
              color: 'white',
              marginBottom: '10px'
            }}>
              Prediction: {results.prediction}
            </h2>

            {/* Confidence */}
            <h3 style={{

              color:
                results.confidence >= 90
                ? '#22c55e'

                : results.confidence >= 70
                ? '#facc15'

                : results.confidence >= 50
                ? '#f97316'

                : '#ef4444',

                marginBottom: '15px'
            }}>
              Confidence: {results.confidence}%
            </h3>

            {/* Confidence Bar Background */}
            <div style={{
              width: '100%',
              height: '20px',
              backgroundColor: '#1e293b',
              borderRadius: '10px',
              overflow: 'hidden'
            }}>

              {/* Confidence Bar Fill */}
              <div style={{
                width: `${results.confidence}%`,
                height: '100%',

                backgroundColor:
                  results.confidence >= 90
                    ? '#22c55e'
                    : results.confidence >= 70
                    ? '#facc15'
                    : results.confidence >=50
                    ? '#f97316'
                    : '#ef4444',

                transition: 'width 0.5s ease'
              }} />

            </div>

          </div>
        )}

      </div>

    </div>
  )
}

export default App
