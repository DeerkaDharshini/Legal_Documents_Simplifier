import React from "react";

function TextInput({ text, setText }) {
  return (
    <textarea
      className="text-input"
      placeholder="Paste legal text here..."
      value={text}
      onChange={(e) => setText(e.target.value)}
    />
  );
}

export default TextInput;