import { Routes, Route} from 'react-router-dom'
import Event from './pages/Event';
import EventList from './pages/EventList';

function App() {
  return (
    <div className="mx-auto min-h-screen max-w-3xl bg-white px-6 py-10 text-slate-900">
      <header className="mb-8 flex items-center justify-between">
        <h1 className="text-4xl font-semibold">Non-Profit Volunteer Management</h1>
      </header>
      <Routes>
        <Route path="/" element={<EventList />} />
        <Route path="/event/:id" element={<Event />} />
      </Routes>
    </div>
  )
}

export default App
