import React, { useState } from "react";
import axios from "axios";

import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";
import TextInput from "../components/TextInput";
import Loader from "../components/Loader";
import ResultCard from "../components/ResultCard";
import AudioPlayer from "../components/AudioPlayer";

function Analyzer() {

  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [simplified, setSimplified] = useState("");
  const [tamil, setTamil] = useState("");
  const [audio, setAudio] = useState("");
  const [loading, setLoading] = useState(false);

  const analyze = async () => {

    if (!text && !file) {
      alert("Enter text or upload file");
      return;
    }

    setLoading(true);

    try {

      if (file) {

        const formData = new FormData();
        formData.append("file", file);

        const res = await axios.post(
          "http://127.0.0.1:8000/upload/",
          formData
        );

        setSimplified(res.data.simplified_text);
        setTamil(res.data.tamil_text);
        setAudio(res.data.audio_url);

      } else {

        const res = await axios.post(
          "http://127.0.0.1:8000/simplify/",
          { text }
        );

        setSimplified(res.data.simplified_text);
        setTamil(res.data.tamil_text);
        setAudio(res.data.audio_url);

      }

    } catch (err) {
      alert("Backend error");
    }

    setLoading(false);
  };

  return (
    <div>

      <Navbar />

      <section className="analyzer">

        <h1>Analyze Legal Document</h1>

        <UploadBox setFile={setFile} />

        <p>OR</p>

        <TextInput text={text} setText={setText} />

        <button onClick={analyze}>
          Analyze Document
        </button>

      </section>

      {loading && <Loader />}

      {simplified && (
        <ResultCard
          title="Simplified English"
          text={simplified}
        />
      )}

      {tamil && (
        <ResultCard
          title="Tamil Translation"
          text={tamil}
        />
      )}

      <AudioPlayer audio={audio} />

    </div>
  );
}

export default Analyzer;