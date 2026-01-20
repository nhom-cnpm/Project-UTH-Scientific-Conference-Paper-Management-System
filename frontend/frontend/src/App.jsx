<<<<<<< HEAD
import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
{
  /* ===== FE2 – Level 1 (Added) ===== */
}
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ReviewerLayout from "./layouts/ReviewerLayout";
import ChairLayout from "./layouts/ChairLayout";
import ReviewerPaperList from "./pages/ReviewerPaperList";
import PaperDetail from "./pages/PaperDetail";
import ChairPaperList from "./pages/ChairPaperList";
export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/reviewer" element={
          <ReviewerLayout>
            <ReviewerPaperList />
          </ReviewerLayout>
        } />

        <Route path="/paper/:id" element={
          <ReviewerLayout>
            <PaperDetail />
          </ReviewerLayout>
        } />

        <Route path="/chair" element={
          <ChairLayout>
            <ChairPaperList />
          </ChairLayout>
        } />

      </Routes>
    </BrowserRouter>
  );
}
{
  /* ===== FE2 ====*/
}
function App() {
  const [count, setCount] = useState(0);

import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
/*>>>>>>> 64f371212420c65bb10c96cc961454fff3857a4c*/

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
<<<<<<< HEAD

    </>
  );
  return <ChairLayout />;
}
export default App;
=======
    </>
  )
}

export default App
/*>>>>>>> 64f371212420c65bb10c96cc961454fff3857a4c*/
