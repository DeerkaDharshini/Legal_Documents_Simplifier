import React from "react";

function UploadBox({ setFile }) {

  const handleFile = (e) => {
    setFile(e.target.files[0]);
  };

  return (
    <div className="upload-box">

      <input
        type="file"
        accept=".pdf,.docx,.txt"
        onChange={handleFile}
      />

      <p>Drag & drop or upload legal document</p>

    </div>
  );
}

export default UploadBox;