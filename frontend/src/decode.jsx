import React, { useState } from 'react';

function DecodeFile() {
  const [downloadLink, setDownloadLink] = useState(null);
  const [fileName, setFileName] = useState('');

  const handleDecode = async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    try {
      const response = await fetch(' http://127.0.0.1:5000/decodefile', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();

      if (result.file_data) {
        const byteCharacters = atob(result.file_data);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);

        const blob = new Blob([byteArray], { type: 'application/octet-stream' }); // Adjust MIME type if needed
        const url = URL.createObjectURL(blob);

        setDownloadLink(url);
        setFileName(result.file_name);
      } else {
        console.error('Error in response:', result.error);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-6">Decode a File from an Image</h1>

      <form
        id="decodeForm"
        onSubmit={handleDecode}
        className="w-full max-w-lg bg-white p-6 rounded-lg shadow-md"
        encType="multipart/form-data"
      >
        <div className="mb-4">
          <label
            htmlFor="img_file"
            className="block text-gray-700 text-sm font-bold mb-2"
          >
            Select Image:
          </label>
          <input
            type="file"
            id="img_file"
            name="img_file"
            accept="image/*"
            required
            className="w-full px-3 py-2 border rounded-lg"
          />
        </div>

        <div className="mb-4">
          <label
            htmlFor="password"
            className="block text-gray-700 text-sm font-bold mb-2"
          >
            Password:
          </label>
          <input
            type="password"
            id="password"
            name="password"
            required
            className="w-full px-3 py-2 border rounded-lg"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-300"
        >
          Decode
        </button>
      </form>

      {downloadLink && (
        <a
          id="download-link"
          href={downloadLink}
          download={fileName}
          className="mt-6 bg-green-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-700 transition duration-300"
        >
          Download File
        </a>
      )}
    </div>
  );
}

export default DecodeFile;
