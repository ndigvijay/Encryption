import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Encode from './encode.jsx';
import Decode from './decode.jsx';

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <Router>
<Routes>
      <Route path="/" element={<Encode />} />
      <Route path="/decode" element={<Decode />} />
</Routes>
  </Router>
);