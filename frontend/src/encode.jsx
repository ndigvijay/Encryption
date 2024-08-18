import React, { useState } from 'react';

function EncodeFile() {
  const [downloadLink, setDownloadLink] = useState(null);
  const [imageFileName, setImageFileName] = useState('');

  const handleEncode = async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    try {
      const response = await fetch(' http://127.0.0.1:5000/encodefile', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setDownloadLink(url);

      const fileInput = document.getElementById('img_file');
      const file = fileInput.files[0];
      setImageFileName(file.name);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-6">Encode a File into an Image</h1>

      <form
        id="encodeForm"
        onSubmit={handleEncode}
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
            htmlFor="zip_file"
            className="block text-gray-700 text-sm font-bold mb-2"
          >
            Select Zip File:
          </label>
          <input
            type="file"
            id="zip_file"
            name="zip_file"
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
          Encode
        </button>
      </form>

      {downloadLink && (
        <a
          id="download-link"
          href={downloadLink}
          download={imageFileName}
          className="mt-6 bg-green-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-700 transition duration-300"
        >
          Download Image
        </a>
      )}
    </div>
  );
}

export default EncodeFile;
