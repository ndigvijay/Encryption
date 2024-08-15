import React, { useState } from 'react';

function App() {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleFileUpload = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    console.log(event.target)
    formData.append('zip_file', event.target.zip_file.files[0]);

    formData.append('image_file', event.target.image_file.files[0]);

    try {
      const res = await fetch('http://127.0.0.1:5000/encode', {
        method: 'POST',
        body: formData,
         headers: {
    'Accept': 'application/json', // Ensures the server returns JSON
  },
      });

      if (!res.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await res.json();
      setResponse(result);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold mb-4">Upload Files</h1>
        <form onSubmit={handleFileUpload} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Upload ZIP File</label>
            <input
              type="file"
              name="zip_file"
              accept=".zip"
              className="mt-1 block w-full text-sm text-gray-900 bg-gray-50 border border-gray-300 rounded-lg cursor-pointer"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Upload Image File</label>
            <input
              type="file"
              name="image_file"
              accept=".jpg,.jpeg,.png"
              className="mt-1 block w-full text-sm text-gray-900 bg-gray-50 border border-gray-300 rounded-lg cursor-pointer"
            />
          </div>
          <button
            type="submit"
            className="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700"
          >
            Upload
          </button>
        </form>
        {response && (
          <div className="mt-4 p-4 bg-green-100 rounded-lg">
            <p>Server Response: {JSON.stringify(response)}</p>
          </div>
        )}
        {error && (
          <div className="mt-4 p-4 bg-red-100 rounded-lg">
            <p>Error: {error}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
